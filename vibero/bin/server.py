# vibero/bin/server.py

import asyncio
import uvicorn
import click
from lagom import Container
from vibero.api import user_games_store
from vibero.api.app import create_api_app
from vibero.core.contextual_correlator import ContextualCorrelator
from vibero.core.loggers import StdoutLogger, Logger, LogLevel
from vibero.core.users import UserStore, UserDocumentStore
from vibero.core.user_games_store import UserGameRepoStore, UserGameRepoDocumentStore
from vibero.adapters.db.postgres import PostgresDB
from vibero.core.common import ASGIApplication


async def setup_container(log_level: str) -> Container:
    container = Container()
    correlator = ContextualCorrelator()
    logger = StdoutLogger(correlator, log_level=LogLevel[log_level.upper()])

    container[ContextualCorrelator] = correlator
    container[Logger] = logger

    db = PostgresDB(logger)
    db.init_db()
    user_store = await UserDocumentStore(db).__aenter__()
    container[UserStore] = user_store

    user_games_store = await UserGameRepoDocumentStore(db).__aenter__()
    container[UserGameRepoStore] = user_games_store

    return container


@click.command()
@click.option("--port", default=8000, help="Port to run the server on.")
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(["debug", "info", "warning", "error", "critical"]),
    help="Logging level.",
)
@click.option(
    "--migrate", is_flag=True, help="Enable database migrations (not implemented yet)."
)
def main(port: int, log_level: str, migrate: bool) -> None:
    async def _run():
        container = await setup_container(log_level)
        app: ASGIApplication = await create_api_app(container)

        config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level=log_level)
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(_run())
