from . import connection
from ...engine import base
from ... import util


class Engine(base.Engine):
    _connection_cls = connection.Connection

    async def _async_init(self):
        return self

    def __await__(self):
        return self._async_init().__await__()

    async def execute(self, statement, *multiparams, **params):
        return await util.awaited(
            self._execute(statement, *multiparams, **params))

    async def contextual_connect(self, close_with_result=False, **kwargs):
        return await util.awaited(
            self._contextual_connect(close_with_result, **kwargs))

    async def _wrap_pool_connect(self, fn, connection):
        return await util.awaited(
            self._wrap_pool_connect_inner(fn, connection))
