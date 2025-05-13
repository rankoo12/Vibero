from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.services.store import store_service

router = APIRouter()

class GameCreate(BaseModel):
    title: str
    description: str | None = None

@router.get("/store/{username}")
def get_user_store(username: str, db: Session = Depends(get_db)):
    return store_service.get_games_by_user(db, username)

@router.post("/store/{username}/game")
def create_game(username: str, game: GameCreate, db: Session = Depends(get_db)):
    return store_service.add_game(db, username, game.title, game.description)

