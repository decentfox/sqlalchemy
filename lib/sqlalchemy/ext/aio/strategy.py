from . import engine
from ...engine.strategies import *
from ... import util


class AsyncioEngineStrategy(DefaultEngineStrategy):
    name = 'asyncio'
    engine_cls = engine.Engine

    async def create(self, name_or_url, **kwargs):
        return await util.awaited(self._create(name_or_url, kwargs))
