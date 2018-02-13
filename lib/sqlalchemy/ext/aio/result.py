from ...engine import result
from ... import util


class ResultProxy(result.ResultProxy):
    async def first(self):
        return await util.awaited(self._first())

    async def scalar(self):
        return await util.awaited(self._scalar())
