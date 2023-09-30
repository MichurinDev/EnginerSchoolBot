# Импорты
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import sqlite3

from modules.markups import *
from modules.config_reader import config

# Объект бота
TOKEN = config.bot_token.get_secret_value()
ADMIN_TOKEN = config.admin_bot_token.get_secret_value()

bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Подгружаем БД
conn = sqlite3.connect('res/data/EnginerSchool.db')
cursor = conn.cursor()


# Состояния бота
class BotStates(StatesGroup):
    START_STATE = State()
    HOME_STATE = State()

    GET_USERNAME_STATE = State()
    GET_CLASS_STATE = State()
    GET_OBJECTS_STATE = State()
    GET_TIMEZONE_STATE = State()


# Переменные для хранения временных данных
_temp = None
user_msg = None


# Хэндлер на команду /start
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    global user_msg

    # Сохраняем экземпляр полдьзовательского сообщения
    user_msg = msg

    # Берём список всех зарегистрированных пользователей с выборков по ID
    user_by_tgID = cursor.execute(f''' SELECT name FROM UsersInfo
                           WHERE tg_id={msg.from_user.id}''').fetchall()

    state = dp.current_state(user=msg.from_user.id)

    if user_by_tgID:
        # Отправляем ее вместе с приветственным сообщением
        # для зарегистрированного пользователя
        await bot.send_message(msg.from_user.id,
                               MENU_TEXT, reply_markup=mainMenu)
        await state.set_state(BotStates.HOME_STATE.state)

    else:
        # Отправляем текст с предложением ввести ФИО
        await bot.send_message(
            msg.from_user.id,
            START_TEXT, reply_markup=types.ReplyKeyboardRemove())

        # Переходим на стадию ввода ФИО
        await bot.send_message(msg.from_user.id, ACQUAINTANCE_TEXT)
        await state.set_state(BotStates.GET_USERNAME_STATE.state)


# Хэндлер на команду /help
@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, HELP_TEXT)


@dp.message_handler(state=BotStates.GET_USERNAME_STATE)
async def get_username(msg: types.Message):
    global _temp

    # Сохраняем имя
    _temp = [msg.text]

    await bot.send_message(
        msg.from_user.id,
        "Выберите класс:",
        reply_markup=keyboard
    )

    # Переходим на стадию ввода класса
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(BotStates.GET_CLASS_STATE.state)


@dp.callback_query_handler(state=BotStates.GET_CLASS_STATE)
async def get_class(callback_query: types.CallbackQuery):
    global _temp

    # Сохраняем класс
    _temp.append(callback_query.data)

    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=None  # Это уберет старую клавиатуру
    )
    await bot.send_message(
        callback_query.from_user.id,
        'Выберете свои предметы:',
        reply_markup=keydoardRepaint(callback_query.data)
    )

    # Переходим на стадию выбора предметов
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(BotStates.GET_OBJECTS_STATE.state)


@dp.callback_query_handler(state=BotStates.GET_OBJECTS_STATE)
async def get_objects(callback_query: types.CallbackQuery):
    global _temp

    # Получаем текущую инлайн-клавиатуру
    current_keyboard = callback_query.message.reply_markup.inline_keyboard

    if callback_query.data in SubjectsList:
        # Находим индекс кнопки, которую хотим изменить
        button_index = None

        for i, row in enumerate(current_keyboard):
            for j, button in enumerate(row):
                if button.callback_data == callback_query.data:
                    button_index = (i, j)
                    break

        # Изменяем текст кнопки, добавляя эмоджи
        if button_index is not None:
            if " ✅" in current_keyboard[button_index[0]][button_index[1]].text:
                current_keyboard[button_index[0]][button_index[1]].text =\
                    callback_query.data.replace(" ✅", "")
            else:
                current_keyboard[button_index[0]][button_index[1]].text =\
                    callback_query.data + " ✅"

        if current_keyboard[-1][0].text != 'ПОЙДЕМ ДАЛЬШЕ ➡️':
            callback_query.message.reply_markup.add(
                InlineKeyboardButton('ПОЙДЕМ ДАЛЬШЕ ➡️',
                                     callback_data='Далее1'))
        # Редактируем сообщение, заменяя только клавиатуру
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=current_keyboard)
        )
    elif callback_query.data == "Далее1":
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=None  # Это уберет старую клавиатуру
        )

        # Сохраняем выбранные предметы
        objects = [k[:-2] for k in list(map(lambda x: x[0].text,
                                            current_keyboard)) if "✅" in k]
        _temp.append(objects)

        # Отправляем сообщение о выборе часового пояса
        await bot.send_message(
            callback_query.from_user.id,
            'Выберите свой часовой пояс:',
            reply_markup=keyboardTimeZone
        )

        # Переходим на стадию выбора предметов
        state = dp.current_state(user=callback_query.from_user.id)
        await state.set_state(BotStates.GET_TIMEZONE_STATE.state)


@dp.callback_query_handler(state=BotStates.GET_TIMEZONE_STATE)
async def get_timezone(callback_query: types.CallbackQuery):
    global _temp

    _temp.append(callback_query.data)

    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=None  # Это уберет старую клавиатуру
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Регистрация успешно завершена!"
    )

    # Создаём запись в БД
    query = f"""INSERT INTO UsersInfo (tg_id, type, name,
    class, subjects, timezone) VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.execute(query,
                   (user_msg.from_user.id, "Ученик", _temp[0],
                    _temp[1], ";".join(_temp[2]), _temp[3]))
    conn.commit()

    _temp = None

    await start(user_msg)


@dp.message_handler(state=BotStates.HOME_STATE)
async def main_menu(msg: types.Message):
    if msg.text == "/start":
        await start(msg)
    elif msg.text == "/help":
        await help(msg)
    elif msg.text == 'Мой профиль 🎓':
        users_data = cursor.execute("""SELECT name, type, class, subjects,
                                    timeZone FROM UsersInfo WHERE tg_id=?""",
                                    (msg.from_user.id,)).fetchall()
        await bot.send_message(
            msg.from_user.id,
            "Данные профиля\n\n" +
            f"ФИО: {users_data[0][0]}\n" +
            f"Тип пользователя: {users_data[0][1]}\n" +
            f"Класс: {users_data[0][2]}\n" +
            f"Часовой пояс: {users_data[0][4]}\n\n" +
            "Предметы:\n- " + '\n- '.join(users_data[0][3].split(";"))
            )
    elif msg.text == 'Мое рассписание 📅':
        await bot.send_message(msg.from_user.id, "Рассписание пользователя")
    elif msg.text == 'Настройки ⚙️':
        await bot.send_message(msg.from_user.id, "Настройки",
                               reply_markup=settingsMenu)
    elif msg.text == 'Сбросить параметры аккаунта 🔄':
        cursor.execute("""DELETE FROM usersInfo WHERE tg_id=?""",
                       (msg.from_user.id,))
        conn.commit()
        await start(user_msg)
    elif msg.text == 'Вернуться назад 🔙':
        await bot.send_message(msg.from_user.id, "Главное меню",
                               reply_markup=mainMenu)


if __name__ == "__main__":
    print("Бот запущен...")
    executor.start_polling(dp, skip_updates=True)
