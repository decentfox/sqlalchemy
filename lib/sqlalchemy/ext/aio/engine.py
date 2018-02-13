from ...engine import base


class Engine(base.Engine):
    async def _async_init(self):
        return self

    def __await__(self):
        return self._async_init().__await__()
