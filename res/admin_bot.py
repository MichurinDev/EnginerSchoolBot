# Импорты
from modules.config_reader import config
from modules.markups import *
from modules.SendNotify import send_notify

from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ParseMode

import sqlite3

TOKEN = config.bot_token.get_secret_value()
ADMIN_TOKEN = config.admin_bot_token.get_secret_value()


# Состояния бота
class BotStates(StatesGroup):
    START_STATE = State()
    HOME_STATE = State()

    CHOICE_CLASS_STATE = State()
    SEND_MESSAGE_STATE = State()


# Объект бота
bot = Bot(token=ADMIN_TOKEN)
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Подгружаем БД
conn = sqlite3.connect('res/data/EnginerSchool.db')
cursor = conn.cursor()

buttons = [
    'Отправить сообщение участникам форума'
]

user_type = ""
_temp = None


# Хэндлер на команду /start
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    global user_type

    # Берём список всех зарегистрированных пользователей с выборков по ID
    user_by_tgID = cursor.execute(f''' SELECT type FROM UsersInfo WHERE
                                  tg_id=? AND type="Администратор"''',
                                  (msg.from_user.id,)).fetchall()

    state = dp.current_state(user=msg.from_user.id)

    if user_by_tgID:
        user_type = user_by_tgID[0][0]

        # Формируем клавиатуру с меню по боту
        menu_keyboard = ReplyKeyboardMarkup()
        for bnt in buttons:
            menu_keyboard.add(KeyboardButton(bnt))

        # Отправляем ее вместе с приветственным сообщением
        # для зарегистрированного пользователя
        if msg.text == "/start":
            await bot.send_message(
                msg.from_user.id, f"Здравсвуйте!")

        await bot.send_message(msg.from_user.id, "Выберите действие:",
                               reply_markup=menu_keyboard)
        await state.set_state(BotStates.HOME_STATE.state)


# Состояние главного меню
@dp.message_handler(state=BotStates.HOME_STATE)
async def home(msg: types.Message):
    if msg.text == buttons[0]:
        if user_type in ['Администратор']:
            admin_classes_kb = ReplyKeyboardMarkup()
            for c in classes:
                admin_classes_kb.add(KeyboardButton(c))
            admin_classes_kb.add("В главное меню")

            await bot.send_message(msg.from_user.id,
                                   "Выберите класс:",
                                   reply_markup=admin_classes_kb)

            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(BotStates.CHOICE_CLASS_STATE.state)
        else:
            await bot.send_message(msg.from_user.id,
                                   ADMINISTRATOR_ACCESS_ERROR)

            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(BotStates.START_STATE.state)
            await start(msg)


# Выбор класса (состояние)
@dp.message_handler(state=BotStates.CHOICE_CLASS_STATE)
async def get_class(msg: types.Message):
    global _temp

    if msg.text != "В главное меню":
        user_class = msg.text

        users = cursor.execute("""SELECT tg_id FROM UsersInfo
                               WHERE type="Ученик" AND class=?""",
                               (user_class,)).fetchall()
        _temp = list(map(lambda x: x[0], users))

        await bot.send_message(msg.from_user.id,
                               "Введите сообщение",
                               reply_markup=ReplyKeyboardMarkup()
                               .add(KeyboardButton("В главное меню")))

        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(BotStates.SEND_MESSAGE_STATE.state)
    else:
        # Выходим в главное меню
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(BotStates.HOME_STATE.state)
        await start(msg)


# Отправка сообщений участникам от лица "клиентского" бота
@dp.message_handler(state=BotStates.SEND_MESSAGE_STATE)
async def send_msg_to_users(msg: types.Message):
    if msg.text != "В главное меню":
        await bot.send_message(msg.from_user.id, "Отправка...")

        # Перебираем ID зарегистрированных пользоателей
        for user in _temp:
            if user != msg.from_user.id:
                # Отправляем сообщение пользователю
                send_notify(token=TOKEN, msg=msg.text, chatId=user)

        await bot.send_message(msg.from_user.id, "Сообщение отправлено!")

    # Выходим в главное меню
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(BotStates.HOME_STATE.state)
    await start(msg)


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    executor.start_polling(dp, skip_updates=False)
