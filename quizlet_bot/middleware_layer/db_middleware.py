from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
from typing import Dict, Any, Awaitable, Callable
from db_core_layer.db_config import get_db


class MyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        async for db in get_db():  # Fetch DB session
            data["db"] = db  # Inject session into handler data
            return await handler(
                event, data
            )  # Pass data to the next middleware_layer/handler
