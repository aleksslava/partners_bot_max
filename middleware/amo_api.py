from __future__ import annotations
from typing import Any, Awaitable, Callable, Dict, Mapping
from maxapi.filters.middleware import BaseMiddleware

from amo_api.amo_api import AmoCRMWrapper

class AmoApiMiddleware(BaseMiddleware):
    def __init__(self, amo_api: AmoCRMWrapper, fields_id: dict) -> None:
        self._amo_api = amo_api
        self.fields_id = fields_id



    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event_object: Any,
        data: dict[str, Any],
    ) -> Any:
        data["amo_api"] = self._amo_api
        data["fields_id"] = self.fields_id

        return await handler(event_object, data)