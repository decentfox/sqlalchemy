import asyncio

from ... import events


class DBAPICursor:
    __slots__ = ['_conn']

    def __init__(self, conn):
        self._conn = conn

    def close(self):
        self._conn = None

    def __getattr__(self, item):
        return getattr(self._conn, item)


class DBAPIConnection:
    __slots__ = ['_pool', '_conn', '_stmt', '_reset_agent']

    def __init__(self, pool, conn):
        self._pool = pool
        self._conn = conn
        self._stmt = None
        self._reset_agent = None

    def cursor(self):
        return DBAPICursor(self)

    def close(self):
        pass


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
