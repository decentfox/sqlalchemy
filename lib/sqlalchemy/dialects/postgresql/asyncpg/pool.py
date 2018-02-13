import asyncpg
from asyncpg.connection import Connection
from asyncpg.prepared_stmt import PreparedStatement

from ....ext.aio import pool


class AnonymousPreparedStatement(PreparedStatement):
    def __del__(self):
        self._state.detach()


class AsyncpgDBAPIConnection(pool.DBAPIConnection):
    async def execute(self, statement, parameters):
        return await self.prepare(statement)

    async def prepare(self, statement, named=True):
        if named:
            rv = await self._conn.prepare(statement)
        else:
            # it may still be a named statement, if cache is not disabled
            # noinspection PyProtectedMember
            self._conn._check_open()
            # noinspection PyProtectedMember
            state = await self._conn._get_statement(statement, None)
            if state.name:
                rv = PreparedStatement(self._conn, statement, state)
            else:
                rv = AnonymousPreparedStatement(self._conn, statement, state)
        self._stmt = rv
        return rv

    @property
    def description(self):
        try:
            return [((a[0], a[1][0]) + (None,) * 5)
                    for a in self._stmt.get_attributes()]
        except TypeError:  # asyncpg <= 0.12.0
            return []

    async def fetchone(self):
        return await self._stmt.fetchrow()


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

    async def connect(self):
        return AsyncpgDBAPIConnection(self, await self._pool.acquire())
