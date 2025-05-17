from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, NewType
from typing_extensions import TypedDict, override
from vibero.adapters.db.models import GameModel
from passlib.context import CryptContext

from vibero.core.persistence.document_database import (
    BaseDocument,
    DocumentDatabase,
    DocumentCollection,
)

GameId = NewType("GameId", str)


@dataclass(frozen=True)
class Game:
    id: GameId
    user_id: str
    title: str
    image: str
    price: float
    discount: float
    created_at: datetime


class UserGameRepoStore(ABC):
    @abstractmethod
    async def get_games_by_username(self, username: str) -> Sequence[Game]: ...


class UserGameRepoDocumentStore(UserGameRepoStore):
    def __init__(self, db: DocumentDatabase, allow_migration: bool = False):
        self._db = db
        self._allow_migration = allow_migration
        self._collection: Optional[DocumentCollection[Game]] = None

    async def __aenter__(self) -> "UserGameRepoDocumentStore":
        self._collection = await self._db.get_or_create_collection(
            name="games",
            schema=Game,
            document_loader=self._document_loader,
            orm_model=GameModel,
        )
        return self

    async def __aexit__(self, *args) -> bool:
        return False

    async def _document_loader(self, doc: BaseDocument) -> Optional[Game]:
        return doc  # trusting DB schema for now

    @override
    async def get_games_by_username(self, username: str) -> Sequence[Game]:
        return await self._collection.find({"username": username})
