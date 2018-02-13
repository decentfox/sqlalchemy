from . import pool
from .. import base


class PGDialect_asyncpg(base.PGDialect):
    poolclass = pool.AsyncpgPool

    @classmethod
    def dbapi(cls):
        from . import dbapi
        return dbapi
