from fastapi import APIRouter, Path, status
from pydantic import Field
from typing import Annotated, Optional, Sequence, TypeAlias

from vibero.core.users import UserStore, UserId
from vibero.core.common import DefaultBaseModel

API_GROUP = "users"

UserIdPath: TypeAlias = Annotated[
    UserId,
    Path(
        description="Unique identifier for the user",
        examples=["usr_123abc"],
        min_length=1,
    ),
]

UsernameField: TypeAlias = Annotated[
    str,
    Field(
        description="Unique username for the user",
        examples=["ran_eck"],
        min_length=3,
        max_length=30,
    ),
]


UserEmailField: TypeAlias = Annotated[
    str,
    Field(
        description="Email address of the user",
        examples=["ran@example.com"],
    ),
]


class UserDTO(DefaultBaseModel):
    id: UserId
    username: UsernameField
    email: UserEmailField
    created_at: str  # Or datetime if your serializer handles it


class UserCreationParamsDTO(DefaultBaseModel):
    username: UsernameField
    email: UserEmailField


class UserUpdateParamsDTO(DefaultBaseModel):
    username: Optional[UsernameField] = None
    email: Optional[UserEmailField] = None


def create_router(user_store: UserStore) -> APIRouter:
    router = APIRouter()

    @router.post(
        "",
        status_code=status.HTTP_201_CREATED,
        response_model=UserDTO,
    )
    async def create_user(params: UserCreationParamsDTO) -> UserDTO:
        user = await user_store.create_user(
            username=params.username,
            email=params.email,
        )
        return UserDTO(**{**user.__dict__, "created_at": user.created_at.isoformat()})

    @router.get(
        "",
        response_model=Sequence[UserDTO],
    )
    async def list_users() -> Sequence[UserDTO]:
        users = await user_store.list_users()
        return [UserDTO(**u.__dict__) for u in users]

    @router.get(
        "/{user_id}",
        response_model=UserDTO,
    )
    async def read_user(user_id: UserIdPath) -> UserDTO:
        user = await user_store.read_user(user_id)
        return UserDTO(**{**user.__dict__, "created_at": user.created_at.isoformat()})

    @router.patch(
        "/{user_id}",
        response_model=UserDTO,
    )
    async def update_user(user_id: UserIdPath, params: UserUpdateParamsDTO) -> UserDTO:
        user = await user_store.update_user(user_id, params.dict(exclude_unset=True))
        return UserDTO(**{**user.__dict__, "created_at": user.created_at.isoformat()})

    @router.delete(
        "/{user_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_user(user_id: UserIdPath) -> None:
        await user_store.delete_user(user_id)

    return router
