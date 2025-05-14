from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, NewType
from typing_extensions import TypedDict

UserId = NewType("UserId", str)


class UserUpdateParams(TypedDict, total=False):
    username: str
    email: str


@dataclass(frozen=True)
class User:
    id: UserId
    username: str
    email: str
    created_at: datetime


class UserStore(ABC):
    @abstractmethod
    async def create_user(self, username: str, email: str) -> User: ...

    @abstractmethod
    async def list_users(self) -> Sequence[User]: ...

    @abstractmethod
    async def read_user(self, user_id: UserId) -> User: ...

    @abstractmethod
    async def update_user(self, user_id: UserId, params: UserUpdateParams) -> User: ...

    @abstractmethod
    async def delete_user(self, user_id: UserId) -> None: ...
