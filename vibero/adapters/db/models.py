from sqlalchemy import Column, String, DateTime, Float
import enum
from sqlalchemy import Enum as PgEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    role = Column(String, nullable=False)


class GameModel(Base):
    __tablename__ = "games"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)  # Optional: denormalized for convenience
    title = Column(String, nullable=False)
    image = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    created_at = Column(DateTime, nullable=False)


class FallbackModel(Base):
    __tablename__ = "fallback"
    id = Column(String, primary_key=True)
