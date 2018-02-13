import pytest
from sqlalchemy import util
from sqlalchemy.testing import fixtures

pytestmark = pytest.mark.asyncio


class TestAwaitGenerator(fixtures.TestBase):
    @pytest.mark.skipif(not util.py35, reason='Python > 3.5 only.')
    async def test_async(self):
        async def error():
            1/0

        def method():
            a = yield 1
            try:
                yield error()
            except ZeroDivisionError:
                pass
            b = yield 2
            raise util.Return(a + b)

        assert await util.awaited(method()) == 3

    async def test_no_return(self):
        def method():
            a = yield 1
            assert a == 1
        await util.awaited(method())

    async def test_no_yield(self):
        def method():
            return 123
        assert await util.awaited(method()) == 123
