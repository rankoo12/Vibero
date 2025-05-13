from pydantic import BaseModel, EmailStr

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
