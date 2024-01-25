from aiogram import types
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import config
from keyboards.KeyboardFactory import KeyboardFactory
from repositories.BotUserRepository import BotUserRepository


class BotGroupMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if message.chat.id == config.admin_chat_id:
            raise CancelHandler