import asyncpg
from asyncpg.connection import Connection

from ....ext.aio import pool


class AsyncpgPool(pool.AsyncPool):
    def __init__(self, creator,
                 dialect=None,
                 loop=None,
                 min_size=10,
                 max_size=10,
                 max_queries=50000,
                 max_inactive_connection_lifetime=300.0,
                 setup=None,
                 init=None,
                 connection_class=Connection,
                 connect_kwargs=None):
        super().__init__(creator, dialect, loop)
        if 'username' in self._kwargs:
            self._kwargs['user'] = self._kwargs.pop('username')
        self._kwargs.update(
            min_size=min_size,
            max_size=max_size,
            max_queries=max_queries,
            max_inactive_connection_lifetime=max_inactive_connection_lifetime,
            setup=setup,
            init=init,
            connection_class=connection_class,
            **({} if connect_kwargs is None else connect_kwargs),
        )
        self._pool = None

    async def _async_init(self):
        self._pool = await asyncpg.create_pool(*self._args, **self._kwargs)
        return self
