from aiogram import types
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from keyboards.KeyboardFactory import KeyboardFactory
from repositories.BotUserRepository import BotUserRepository


class UserAuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        data['data'] = {}
        user = BotUserRepository.get_user_by_telegram_id(message.from_user.id)

        if message.content_type == 'contact' or message.get_command(True) == 'help' or message.get_command(True) == 'start':
            data['data']['user'] = user
            return

        if not user:
            await message.reply('Пожалуйста, предоставьте номер телефона для корректной работы бота, а затем повторите команду еще раз. Сделать это можно отправив контакт.', reply_markup=KeyboardFactory.build('contact'))
            raise CancelHandler
        user = user.load('driver', 'driver.park', 'driver.park.session')

        if not user.driver.car_id:
            await message.reply('Водитель с данным номером телефона, не имеет привязанного автомобиля, обратитесь в парк')
            raise CancelHandler

        data['data']['user'] = user
        data['data']['driver'] = user.driver
        data['data']['park'] = user.driver.park
        data['data']['session'] = user.driver.park.session