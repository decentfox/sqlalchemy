import pytest
from asyncpg import pool
from sqlalchemy.testing import fixtures
from sqlalchemy.testing import config

pytestmark = pytest.mark.asyncio


class EngineTest(fixtures.TestBase):
    __only_on__ = 'postgresql'

    async def test_strategy(self):
        url = str(config.db_url).replace('postgresql://', 'asyncpg://')
        from sqlalchemy import create_engine
        e = await create_engine(url, strategy='asyncio')
        assert isinstance(e.pool._pool, pool.Pool)
