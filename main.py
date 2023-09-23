# Импорты
from aiogram import Bot, Dispatcher, executor, types
from res.markups import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from res.config_reader import config

# Объект бота
TOKEN = config.bot_token.get_secret_value()
ADMIN_TOKEN = config.admin_bot_token.get_secret_value()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.answer(text="Выберите класс:", reply_markup=keyboard)


@dp.callback_query_handler()
async def choosingTrainingClass(callback_query: types.CallbackQuery):
    if callback_query.data in classes:
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

    elif callback_query.data in SubjectsList:
        # Получаем текущую инлайн-клавиатуру
        current_keyboard = callback_query.message.reply_markup.inline_keyboard

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
    if callback_query.data == "Далее1":
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=None  # Это уберет старую клавиатуру
        )
        await bot.send_message(
            callback_query.from_user.id,
            'Выберите свой часовой пояс:',
            reply_markup=keyboardTimeZone
        )
    if callback_query.data in TimeZonesList:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=None  # Это уберет старую клавиатуру
        )
        await bot.send_message(callback_query.from_user.id,
                               "Регистрация успешно завершена!",
                               reply_markup=mainMenu)


@dp.message_handler(Text(equals=[
    "Мой профиль 🎓",
    "Мое рассписание 📅",
    "Настройки ⚙️",
    "Вернуться назад 🔙",
    "Сбросить параметры аккаунта 🔄"
    ]))
async def mainMenu(message: types.Message):
    # Сообение при нажатии на "мой профиль"
    if message.text == 'Мой профиль 🎓':
        await message.answer(text="Данные профиля:\n" +
                             "Класс:\nПредметы:\nЧасовой пояс")
    elif message.text == 'Мое рассписание 📅':
        await message.answer(text="Рассписание пользователя")
    elif message.text == 'Настройки ⚙️':
        await message.answer(text="Настройки", reply_markup=settingsMenu)
    elif message.text == 'Сбросить параметры аккаунта 🔄':
        await message.answer(text="Сбросить настройки")
    elif message.text == 'Вернуться назад 🔙':
        await message.answer(text="Главное меню", reply_markup=mainMenu)


if __name__ == "__main__":
    print("Бот запущен...")
    executor.start_polling(dp, skip_updates=True)
