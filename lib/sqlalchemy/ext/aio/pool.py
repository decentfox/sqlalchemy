import asyncio

from ... import events


class AsyncPool:
    def __init__(self, creator, dialect=None, loop=None):
        self._args, self._kwargs = creator()
        self.dialect = dialect
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

    def __init_subclass__(cls, **kwargs):
        class AsyncPoolEvents(events.PoolEvents):
            _dispatch_target = cls

    async def _async_init(self):
        return self

    def __await__(self):
        return self._async_init().__await__()
