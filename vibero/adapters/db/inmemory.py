from __future__ import annotations
from typing import Awaitable, Callable, Optional, Sequence, cast
from typing_extensions import override, get_type_hints
from vibero.core.users import User, UserId, UserStore, UserUpdateParams
from vibero.core.persistence.common import ObjectId
from vibero.core.common import generate_id
from datetime import datetime
from typing import Sequence

from vibero.core.persistence.common import (
    matches_filters,
    Where,
    ObjectId,
    ensure_is_total,
)
from vibero.core.persistence.document_database import (
    BaseDocument,
    DeleteResult,
    DocumentCollection,
    DocumentDatabase,
    InsertResult,
    TDocument,
    UpdateResult,
)


class InMemoryDocumentDatabase(DocumentDatabase):
    def __init__(self) -> None:
        self._collections: dict[str, InMemoryDocumentCollection[BaseDocument]] = {}

    @override
    async def create_collection(
        self,
        name: str,
        schema: type[TDocument],
    ) -> InMemoryDocumentCollection[TDocument]:
        annotations = get_type_hints(schema)
        assert "id" in annotations

        self._collections[name] = InMemoryDocumentCollection(name=name, schema=schema)
        return cast(InMemoryDocumentCollection[TDocument], self._collections[name])

    @override
    async def get_collection(
        self,
        name: str,
        schema: type[TDocument],
        document_loader: Callable[[BaseDocument], Awaitable[Optional[TDocument]]],
    ) -> InMemoryDocumentCollection[TDocument]:
        if name in self._collections:
            return cast(InMemoryDocumentCollection[TDocument], self._collections[name])
        raise ValueError(f'Collection "{name}" does not exist')

    @override
    async def get_or_create_collection(
        self,
        name: str,
        schema: type[TDocument],
        document_loader: Callable[[BaseDocument], Awaitable[Optional[TDocument]]],
    ) -> InMemoryDocumentCollection[TDocument]:
        if collection := self._collections.get(name):
            return cast(InMemoryDocumentCollection[TDocument], collection)

        return await self.create_collection(name=name, schema=schema)

    @override
    async def delete_collection(self, name: str) -> None:
        if name in self._collections:
            del self._collections[name]
        else:
            raise ValueError(f'Collection "{name}" does not exist')


class InMemoryDocumentCollection(DocumentCollection[TDocument]):
    def __init__(
        self,
        name: str,
        schema: type[TDocument],
        data: Optional[Sequence[TDocument]] = None,
    ) -> None:
        self._name = name
        self._schema = schema
        self._documents = list(data) if data else []

    @override
    async def find(self, filters: Where) -> Sequence[TDocument]:
        return [
            doc for doc in self._documents if matches_filters(filters, doc.__dict__)
        ]

    @override
    async def find_one(self, filters: Where) -> Optional[TDocument]:
        for doc in self._documents:
            if matches_filters(filters, doc.__dict__):
                return doc
        return None

    @override
    async def insert_one(self, document: TDocument) -> InsertResult:
        ensure_is_total(document.__dict__, self._schema)
        self._documents.append(document)
        return InsertResult(acknowledged=True)

    @override
    async def update_one(
        self,
        filters: Where,
        params: TDocument,
        upsert: bool = False,
    ) -> UpdateResult[TDocument]:
        for i, doc in enumerate(self._documents):
            if matches_filters(filters, doc.__dict__):
                updated = cast(TDocument, {**self._documents[i], **params})
                self._documents[i] = updated
                return UpdateResult(
                    acknowledged=True,
                    matched_count=1,
                    modified_count=1,
                    updated_document=updated,
                )

        if upsert:
            await self.insert_one(params)
            return UpdateResult(
                acknowledged=True,
                matched_count=0,
                modified_count=0,
                updated_document=params,
            )

        return UpdateResult(
            acknowledged=True,
            matched_count=0,
            modified_count=0,
            updated_document=None,
        )

    @override
    async def delete_one(self, filters: Where) -> DeleteResult[TDocument]:
        for i, doc in enumerate(self._documents):
            if matches_filters(filters, doc.__dict__):
                removed = self._documents.pop(i)
                return DeleteResult(
                    acknowledged=True,
                    deleted_count=1,
                    deleted_document=removed,
                )

        return DeleteResult(
            acknowledged=True,
            deleted_count=0,
            deleted_document=None,
        )


class InMemoryUserStore(UserStore):
    def __init__(self) -> None:
        self._db = InMemoryDocumentDatabase()
        self._users: InMemoryDocumentCollection[User] = None  # will init lazily

    async def _ensure_collection(self) -> None:
        if self._users is None:
            self._users = await self._db.get_or_create_collection(
                name="users",
                schema=User,
                document_loader=lambda doc: doc,  # Not used in memory
            )

    async def create_user(self, username: str, email: str) -> User:
        await self._ensure_collection()
        user = User(
            id=UserId(generate_id()),
            username=username,
            email=email,
            created_at=datetime.utcnow(),
        )
        await self._users.insert_one(user)
        return user

    async def list_users(self) -> Sequence[User]:
        await self._ensure_collection()
        return await self._users.find({})

    async def read_user(self, user_id: UserId) -> User:
        await self._ensure_collection()
        user = await self._users.find_one({"id": {"$eq": user_id}})
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user

    async def update_user(self, user_id: UserId, params: UserUpdateParams) -> User:
        await self._ensure_collection()
        updated = await self._users.update_one({"id": {"$eq": user_id}}, params)
        if updated.updated_document is None:
            raise ValueError(f"User with ID {user_id} not found")
        return updated.updated_document

    async def delete_user(self, user_id: UserId) -> None:
        await self._ensure_collection()
        deleted = await self._users.delete_one({"id": {"$eq": user_id}})
        if deleted.deleted_count == 0:
            raise ValueError(f"User with ID {user_id} not found")
