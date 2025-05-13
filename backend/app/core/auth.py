from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from api.types import UserCreateDTO, UserLoginDTO, TokenDTO


def register_user(user_data: UserCreateDTO, db: Session) -> TokenDTO:
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.username})
    return TokenDTO(access_token=token)

def login_user(credentials: UserLoginDTO, db: Session) -> TokenDTO:
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    return TokenDTO(access_token=token)
