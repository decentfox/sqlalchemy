import asyncpg

paramstyle = 'numeric'
Error = asyncpg.PostgresError, asyncpg.InterfaceError


def connect(*args, **kwargs):
    return args, kwargs
