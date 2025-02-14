from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
from typing import Dict, Any, Awaitable, Callable


class UserIDExtractorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
        elif event.inline_query:
            user_id = event.inline_query.from_user.id
        else:
            user_id = None
        if user_id:
            data["injected_user_id"] = str(user_id)
