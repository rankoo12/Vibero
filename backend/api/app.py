import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.index import create_api_router
from app.core.database import Base, engine
from app.models import user, game
from contextlib import asynccontextmanager
from api import store

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔁 Running lifespan startup")
    Base.metadata.create_all(bind=engine)
    yield

def create_api_app() -> FastAPI:
    frontend_origin = os.getenv("FRONTEND_ORIGIN")
    if not frontend_origin:
        raise RuntimeError("❌ FRONTEND_ORIGIN not set in .env")

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(create_api_router())
    app.include_router(store.router)

    return app
