import asyncio
import inspect

from .langhelpers import Return


async def awaited(gen):
    if not inspect.isgenerator(gen):
        return gen
    result = None
    exception = None
    try:
        while True:
            if exception is None:
                result = gen.send(result)
            else:
                result = gen.throw(exception)
                exception = None
            if asyncio.isfuture(result) or \
                    asyncio.iscoroutine(result) or \
                    inspect.isawaitable(result):
                try:
                    result = await result
                except Exception as e:
                    exception = e
    except Return as e:
        return e.value
    except StopIteration:
        pass
