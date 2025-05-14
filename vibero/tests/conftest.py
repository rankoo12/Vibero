import pytest
import pytest_asyncio
from lagom import Container
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typing import AsyncIterator

from vibero.api.app import create_api_app, ASGIApplication
from vibero.core.loggers import Logger, StdoutLogger
from vibero.core.contextual_correlator import ContextualCorrelator
from vibero.core.users import UserStore

from vibero.adapters.db.inmemory import InMemoryUserStore


@pytest.fixture
def container() -> Container:
    container = Container()
    container[ContextualCorrelator] = ContextualCorrelator()
    container[Logger] = StdoutLogger(correlator=container[ContextualCorrelator])
    container[UserStore] = InMemoryUserStore()
    return container


@pytest_asyncio.fixture
async def api_app(container: Container) -> ASGIApplication:
    return await create_api_app(container)


@pytest_asyncio.fixture
async def async_client(api_app: ASGIApplication) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=api_app), base_url="http://test"
    ) as client:
        yield client
