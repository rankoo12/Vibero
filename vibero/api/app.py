from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, status
import os
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import Callable, Awaitable, TypeAlias
from starlette.types import Receive, Scope, Send
import uuid
from lagom import Container
from vibero.core.common import generate_id, ItemNotFoundError
from vibero.core.contextual_correlator import ContextualCorrelator
from vibero.core.loggers import Logger
from vibero.api import users
from vibero.core.users import UserStore

ASGIApplication: TypeAlias = Callable[[Scope, Receive, Send], Awaitable[None]]
frontend_origin = os.getenv("FRONTEND_ORIGIN")
if not frontend_origin:
    raise RuntimeError("FRONTEND_ORIGIN is not set in the environment.")


class AppWrapper:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            return await self.app(scope, receive, send)
        except asyncio.CancelledError:
            pass


async def create_api_app(container: Container) -> ASGIApplication:
    correlator = container[ContextualCorrelator]
    logger = container[Logger]
    user_store = container[UserStore]

    api_app = FastAPI()

    @api_app.middleware("http")
    async def handle_cancellation(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            return await call_next(request)
        except asyncio.CancelledError:
            return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api_app.middleware("http")
    async def add_correlation_id(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.url.path.startswith("/chat/"):
            return await call_next(request)

        request_id = generate_id()
        with correlator.correlation_scope(f"RID({request_id})"):
            with logger.operation(f"HTTP Request: {request.method} {request.url.path}"):
                return await call_next(request)

    @api_app.exception_handler(ItemNotFoundError)
    async def item_not_found_error_handler(
        request: Request, exc: ItemNotFoundError
    ) -> HTTPException:
        logger.info(str(exc))

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    users_router = APIRouter(prefix="/users")
    users_router.include_router(
        router=users.create_router(user_store=user_store),
        prefix="/users",
        tags=["users"],
    )

    api_app.include_router(
        users.create_router(user_store=user_store),
        prefix="/users",
        tags=["users"],
    )

    return AppWrapper(api_app)
