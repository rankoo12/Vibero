from fastapi import APIRouter, Path, status, Response, HTTPException, Request
from pydantic import Field
from typing import Annotated, Optional, Sequence, TypeAlias, Literal
import enum

from vibero.core.users import UserStore, UserId
from vibero.core.common import DefaultBaseModel
from vibero.core.security import (
    create_session_token,
    verify_session_token,
    verify_password,
)

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


class UserRole(str, enum.Enum):
    regular = "regular"
    publisher = "publisher"


UserRoleField: TypeAlias = Annotated[
    Literal[UserRole.regular, UserRole.publisher],
    Field(description="Role of the user", examples=[UserRole.regular.value]),
]


class UserDTO(DefaultBaseModel):
    id: UserId
    username: UsernameField
    email: UserEmailField
    created_at: str
    role: str


class UserCreationParamsDTO(DefaultBaseModel):
    username: UsernameField
    email: UserEmailField
    password: Annotated[str, Field(min_length=6, max_length=128)]
    role: UserRoleField = Field(
        default=UserRole.regular,
        description="Role of the user (e.g., regular or publisher)",
    )


class UserUpdateParamsDTO(DefaultBaseModel):
    username: Optional[UsernameField] = None
    email: Optional[UserEmailField] = None


class LoginDTO(DefaultBaseModel):
    password: Annotated[str, Field(min_length=6, max_length=128)]


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
            password=params.password,
        )
        return UserDTO(**{**user.__dict__, "created_at": user.created_at.isoformat()})

    @router.get(
        "",
        response_model=Sequence[UserDTO],
    )
    async def list_users() -> Sequence[UserDTO]:
        users = await user_store.list_users()
        return [UserDTO(**u.__dict__) for u in users]

    @router.get("/session", response_model=UserDTO)
    async def read_session(request: Request) -> UserDTO:
        session_token = request.cookies.get("session")
        if not session_token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        user_id = verify_session_token(session_token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid session token")

        user = await user_store.read_user(user_id)
        return UserDTO(**{**user.__dict__, "created_at": user.created_at.isoformat()})

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
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at.isoformat(),
        )

    @router.delete(
        "/{user_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_user(user_id: UserIdPath) -> None:
        await user_store.delete_user(user_id)

    @router.post(
        "/{username}/login",
        response_model=UserDTO,
        status_code=status.HTTP_200_OK,
    )
    async def user_login(
        username: str, params: LoginDTO, response: Response
    ) -> UserDTO:
        user = await user_store.get_by_username(username)
        if not verify_password(params.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_token = create_session_token(user.id)

        response.set_cookie(
            key="session",
            value=session_token,
            httponly=True,
            secure=False,  # True in production
            samesite="Lax",
            max_age=60 * 60 * 24 * 7,
        )

        return UserDTO(**{**user.__dict__, "created_at": user.created_at.isoformat()})

    @router.post(
        "/{username}/logout",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def logout_user(response: Response) -> None:
        response.delete_cookie("session")

    return router
