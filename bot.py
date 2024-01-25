import config
import os

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from phonenumbers import NumberParseException

from keyboards.KeyboardFactory import KeyboardFactory
from middlewares.BotGroupMiddleware import BotGroupMiddleware
from middlewares.UserAuthMiddleware import UserAuthMiddleware
from repositories.BotUserRepository import BotUserRepository
from repositories.PhoneRepository import PhoneRepository
from services.BotService import BotService
from helpers import format_phone
from states.ChangeCarState import ChangeCarState


bot = Bot(token=config.bot_token)

storage = JSONStorage('storage.json')
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['help', 'start'])
async def help_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Данный бот позволяет управлять настройками вашего профиля в Яндекс Такси, для работы используйте команды которые появляются по нажатию в поле ввода.')
    await message.reply(
        'Пожалуйста, предоставьте номер телефона для корректной работы бота. Сделать это можно отправив контакт.',
        reply_markup=KeyboardFactory.build('contact'))


@dp.message_handler(commands=['nal'])
async def nal(message: types.Message, data: dict):
    bot_service = BotService(data)
    if bot_service.nal():
        await bot.send_message(message.chat.id, 'Безнал включен')
    else:
        await bot.send_message(message.chat.id, 'Безнал выключен')


@dp.message_handler(commands=['booster'])
async def booster(message: types.Message, data: dict):
    bot_service = BotService(data)
    # Выключим тариф детский без бустера
    # if data['user'].kids:
    #    bot_service.child_seat()

    if bot_service.booster():
        await bot.send_message(message.chat.id, 'Бустер включен')
    else:
        await bot.send_message(message.chat.id, 'Бустер отключен')


@dp.message_handler(commands=['brand'])
async def brand(message: types.Message, data: dict):
    bot_service = BotService(data)
    if bot_service.brand():
        await bot.send_message(message.chat.id, 'Бренд включен')
    else:
        await bot.send_message(message.chat.id, 'Бренд выключен')


@dp.message_handler(commands=['kids'])
async def kids(message: types.Message, data: dict):
    data['user'].booster = True
    bot_service = BotService(data)
    # Если есть бустер, выключим
    # if data['user'].booster:
    #    bot_service.booster()

    if bot_service.child_seat():
        await bot.send_message(message.chat.id, 'Тариф детский включен')
    else:
        await bot.send_message(message.chat.id, 'Тариф детский отключен')


@dp.message_handler(commands=['change_car'])
async def change_car(message: types.Message):
    await ChangeCarState.name.set()
    await bot.send_message(message.chat.id,
                           'Для смены автомобиля, пожалуйста отправьте ваше ФИО и название парка в ответном сообщении. Либо вы можете отменить создание заявки /cancel_car_change')


@dp.message_handler(state='*', commands='cancel_car_change')
async def cancel_car_change(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await bot.send_message(message.chat.id, 'Заявка на смену автомобиля отменена')
    await state.finish()


@dp.message_handler(state=ChangeCarState.name)
async def change_car_handle_name(message: types.Message, state: FSMContext):
    if not message.text or message.text[0] == '/':
        await bot.send_message(message.chat.id, 'Пожалуйста укажите ФИО и название парка')
        return

    async with state.proxy() as data:
        data['name'] = message.text
    await ChangeCarState.next()
    await bot.send_message(message.chat.id,
                           'Пожалуйста отправьте фото СТС вашего автомобиля, либо вы можете отменить создание заявки /cancel_car_change')


@dp.message_handler(content_types=['photo', 'text'], state=ChangeCarState.photo)
async def change_car_handle_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await bot.send_message(message.chat.id,
                               'Пожалуйста отправьте фото СТС вашего автомобиля, либо вы можете отменить создание заявки /cancel_car_change')
        return

    async with state.proxy() as data:
        await bot.send_message(message.chat.id, 'Спасибо за предоставление информации, ваша заявка отправлена.')
        await bot.send_message(config.admin_chat_id, f'*Заявка на изменение автомобиля.*\n\nФИО и название парка: {data["name"]}\nАккаунт: {message.from_user.mention}\n\nФото СТС ниже', parse_mode='Markdown')
        await message.photo[-1].download(message.photo[-1].file_id + '.jpg')
        await bot.send_photo(config.admin_chat_id, photo=open(message.photo[-1].file_id + '.jpg', 'rb'))
        os.remove(message.photo[-1].file_id + '.jpg')

    await state.finish()


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message, data: dict):
    try:
        phone_number = format_phone(message.contact.phone_number)
    except NumberParseException as e:
        await bot.send_message(message.chat.id, 'Не удалось обработать номер, вероятно он неправильный')
        return

    if data['user'] or BotUserRepository.get_user_by_phone(phone_number):
        await bot.send_message(message.chat.id, 'Вы уже зарегистрированы',
                               reply_markup=KeyboardFactory.build('remove_keyboard'))
        return
    if message.from_user.id == message.contact.user_id:
        phones = PhoneRepository.get_phones(phone_number)
        if len(phones) > 1:
            await bot.send_message(message.chat.id,
                                   'Найдено более одного водителя с таким номером телефона, пожалуйста обратитесь в парк',
                                   reply_markup=KeyboardFactory.build('remove_keyboard'))
            return
        if len(phones) == 1:
            BotUserRepository.create_user(telegram_user_id=message.contact.user_id, driver_id=phones.first().driver.id,
                                          phone=phones.first().phone)
            await bot.send_message(message.chat.id, 'Благодарим вас, теперь вы можете пользоваться ботом',
                                   reply_markup=KeyboardFactory.build('remove_keyboard'))
        else:
            await bot.send_message(message.chat.id, 'Водитель с данным номером телефона не найден',
                                   reply_markup=KeyboardFactory.build('remove_keyboard'))
    else:
        await bot.send_message(message.chat.id, 'Вы отправили чужой контакт',
                               reply_markup=KeyboardFactory.build('remove_keyboard'))


dp.middleware.setup(BotGroupMiddleware())
dp.middleware.setup(UserAuthMiddleware())
executor.start_polling(dp)
