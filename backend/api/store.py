from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user_from_cookie
from app.core.services.store import store_service
from app.models.user import User

router = APIRouter()

class GameCreate(BaseModel):
    title: str
    description: str | None = None

@router.get("/store/{username}")
def get_user_store(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie),
):
    if username != current_user.username:
        raise HTTPException(status_code=403, detail="Not your store")
    
    return store_service.get_games_by_user(db, username)

@router.post("/store/{username}/game")
def create_game(
    username: str,
    game: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie),
):
    if username != current_user.username:
        raise HTTPException(status_code=403, detail="Not your store")

    return store_service.add_game(db, username, game.title, game.description)
