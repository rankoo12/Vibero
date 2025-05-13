from fastapi import APIRouter
from api.auth import create_router as create_auth_router
# later:
# from api.games import create_router as create_games_router
# from api.store import create_router as create_store_router

def create_api_router() -> APIRouter:
    router = APIRouter()

    router.include_router(create_auth_router())
    # router.include_router(create_games_router())
    # router.include_router(create_store_router())

    return router
