from fastapi import APIRouter, Path, HTTPException
from typing import Annotated, Sequence
from vibero.core.user_games_store import UserGameRepoStore, Game  # ✅ renamed import
from vibero.core.common import DefaultBaseModel

UsernamePath = Annotated[
    str,
    Path(
        description="Unique username of the user who owns the store",
        examples=["ran_eck"],
        min_length=3,
        max_length=30,
    ),
]


class GameDTO(DefaultBaseModel):
    id: str
    title: str
    image: str
    price: float
    discount: float


def create_router(game_repository: UserGameRepoStore) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/{username}/games",
        response_model=Sequence[GameDTO],
    )
    async def get_user_games(username: UsernamePath) -> Sequence[GameDTO]:
        try:
            games = await game_repository.get_games_by_username(username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        return [
            GameDTO(**g.__dict__, created_at=g.created_at.isoformat()) for g in games
        ]

    return router
