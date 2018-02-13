from ...engine import base
from ... import util


class Connection(base.Connection):
    async def _execute_context(self, dialect, constructor,
                               statement, parameters,
                               *args):
        return await util.awaited(
            self._execute_context_inner(dialect, constructor, statement,
                                        parameters, *args))

    async def _execute_text(self, statement, multiparams, params):
        return await util.awaited(
            self._execute_text_inner(statement, multiparams, params))
