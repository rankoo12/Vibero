from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.auth import register_user, login_user
from app.core.deps import get_db
from api.types import UserCreateDTO, UserLoginDTO, TokenDTO


class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"

def create_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post("/register", response_model=TokenDTO, status_code=201)
    def register(user: UserCreateDTO, db: Session = Depends(get_db)):
        return register_user(user, db)

    @router.post("/login", response_model=TokenDTO)
    def login(credentials: UserLoginDTO, db: Session = Depends(get_db)):
        return login_user(credentials, db)

    return router
