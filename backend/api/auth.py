from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.auth import register_user, login_user
from app.core.deps import get_db, get_current_user_from_cookie
from api.types import UserCreateDTO, UserLoginDTO, TokenDTO, UserInfoDTO

def create_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post("/register", response_model=TokenDTO, status_code=201)
    def register(user: UserCreateDTO, db: Session = Depends(get_db)):
        return register_user(user, db)

    @router.post("/login")
    def login(credentials: UserLoginDTO, db: Session = Depends(get_db)):
        token_data = login_user(credentials, db)  # This returns a TokenDTO (token string)
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(
        key="access_token",
        value=token_data.access_token,
        httponly=True,
        secure=False,  # ✅ Set to True in production with HTTPS
        samesite="lax",
        max_age=3600,
        path="/"        # ✅ Important to allow the cookie across all routes
    )

        return response
    @router.get("/login", response_model=UserInfoDTO)
    def get_logged_in_user(current_user: User = Depends(get_current_user_from_cookie)):
        return {"username": current_user.username}

    return router
