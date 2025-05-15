from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, NewType
from typing_extensions import TypedDict, override
from vibero.adapters.db.models import UserModel
from passlib.context import CryptContext

from vibero.core.persistence.document_database import (
    BaseDocument,
    DocumentDatabase,
    DocumentCollection,
)

UserId = NewType("UserId", str)


class UserUpdateParams(TypedDict, total=False):
    username: str
    email: str


@dataclass(frozen=True)
class User:
    id: UserId
    username: str
    email: str
    hashed_password: str
    created_at: datetime


class UserStore(ABC):
    @abstractmethod
    async def create_user(self, username: str, email: str) -> User: ...

    @abstractmethod
    async def list_users(self) -> Sequence[User]: ...

    @abstractmethod
    async def read_user(self, user_id: UserId) -> User: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...

    @abstractmethod
    async def update_user(self, user_id: UserId, params: UserUpdateParams) -> User: ...

    @abstractmethod
    async def delete_user(self, user_id: UserId) -> None: ...


class UserDocumentStore(UserStore):
    def __init__(self, db: DocumentDatabase, allow_migration: bool = False):
        self._db = db
        self._allow_migration = allow_migration
        self._collection: Optional[DocumentCollection[User]] = None

    async def __aenter__(self) -> "UserDocumentStore":
        self._collection = await self._db.get_or_create_collection(
            name="users",
            schema=User,
            document_loader=self._document_loader,
            orm_model=UserModel,
        )
        return self

    async def __aexit__(self, *args) -> bool:
        return False

    async def _document_loader(self, doc: BaseDocument) -> Optional[User]:
        return doc  # trusting structure, no migrations yet

    @override
    async def create_user(self, username: str, email: str, password: str) -> User:
        from vibero.core.common import generate_id

        pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_ctx.hash(password)

        user = User(
            id=UserId(generate_id()),
            username=username,
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
        )
        await self._collection.insert_one(user)
        return user

    @override
    async def list_users(self) -> list[User]:
        return await self._collection.find({})

    @override
    async def read_user(self, user_id: UserId) -> User:
        user = await self._collection.find_one({"id": user_id})
        if user is None:
            raise ValueError(f"User with id '{user_id}' not found")
        return user

    @override
    async def get_by_username(self, username: str) -> User:
        user = await self._collection.find_one({"username": username})
        if user is None:
            raise ValueError(f"User with username '{username}' not found")
        return user

    @override
    async def update_user(self, user_id: UserId, params: UserUpdateParams) -> User:
        result = await self._collection.update_one({"id": user_id}, params)
        doc = result.updated_document

        if doc is None:
            raise ValueError(f"Failed to update user with id '{user_id}'")

        return User(
            id=UserId(doc.id),
            username=doc.username,
            email=doc.email,
            created_at=doc.created_at,
        )

    @override
    async def delete_user(self, user_id: UserId) -> None:
        await self._collection.delete_one({"id": user_id})
