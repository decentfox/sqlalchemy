from . import pool
from ..base import PGExecutionContext
from .. import base
from ....ext.aio import result


class PGExecutionContext_asyncpg(PGExecutionContext):
    def get_result_proxy(self):
        return result.ResultProxy(self)


class PGDialect_asyncpg(base.PGDialect):
    poolclass = pool.AsyncpgPool
    execution_ctx_cls = PGExecutionContext_asyncpg

    @classmethod
    def dbapi(cls):
        from . import dbapi
        return dbapi

    async def do_execute(self, cursor, statement, parameters, context=None):
        await cursor.execute(statement, parameters)
