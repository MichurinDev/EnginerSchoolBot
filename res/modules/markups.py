from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3

# Подгружаем БД
conn = sqlite3.connect('res/data/EnginerSchool.db')
cursor = conn.cursor()

# --- Тексты ---
START_TEXT = \
    f"""
<b>Привет! Это бот Цифриума, который подскажет тебе расписание занятий.</b>


Я новенький чат-бот и у пока не так много умею, поэтому если ты не можешь найти ответ на свой вопрос - посмотри информацию на сайте школы https://будущие-инженеры.рф или обратись в техническую поддержку через кнопку на сайте.


Вот инструкция по работе с ботом:

<i>Регистрация ✅</i>
1. Переходи по ссылке на бота и запускай его нажатием кнопки "Старт" снизу.
3. Выбирай класс: нажимай на кнопки в диалоге.
4. Выбирай курсы, на которых ты будешь обучаться: нажимай на кнопки в диалоге.
5. Выбирай свой часовой пояс
РЕГИСТРАЦИЯ ЗАВЕРШЕНА.

<b><i>Использование</i></b> 💬
1. Появляются кнопки, замещающие клавиатуру
2. При нажатии на кнопку "Профиль", ты увидишь свои данные: класс, предметы
3. При нажатии на кнопку "Расписание" тебе откроется расписание на текущую неделю
4. Если ты неправильно ввел данные, то можно пройти регистрацию заново: «Настройки» → «Сбросить данные профиля»

Чтобы я смог показывать тебе расписание, выполни несколько простых действий

По вопросам работоспособности бота пишите в личные сообщения @michurin_offic
"""

MENU_TEXT = "Выберите действие 🚀"

ACQUAINTANCE_TEXT = "Выберите класс 👨‍🎓"

HELP_TEXT = \
    """
Инструкция:
Регистрация
1. Переходи по ссылке на бота и запускай его нажатием кнопки "Старт" снизу.
2. Выбирай класс: нажимай на кнопки в диалоге.
3. Выбирай курсы, на которых ты будешь обучаться: нажимай на кнопки в диалоге.
4. Выбирай свой часовой пояс
РЕГИСТРАЦИЯ ЗАВЕРШЕНА.

Использование
1. Появляются кнопки, замещающие клавиатуру
2. При нажатии на кнопку "Профиль", ты увидишь свои данные: класс, предметы
3. При нажатии на кнопку "Расписание" тебе откроется расписание на текущую неделю
4. Если ты неправильно ввел данные, то можно пройти регистрацию заново: "Настройки" => "Сбросить данные профиля"

По вопросам работоспособности бота пишите в личные сообщения @michurin_offic
"""

ADMINISTRATOR_ACCESS_ERROR = \
    """
У вас недостаточно прав для выполнения данного действия!
"""

NOTIFY_PATTERN_TEXT = """"""


def keydoardRepaint(nameMarkup):
    new_buttons = buttons[nameMarkup]
    # Разбиваем кнопки на две строки (по 2 кнопки в каждой)
    button_rows = [new_buttons[i:i + 2] for i in range(0, len(new_buttons), 2)]

    # Добавляем кнопки в инлайновую клавиатуру
    keyboard = InlineKeyboardMarkup(row_width=1)
    for row in button_rows:
        keyboard.add(*row)
    return keyboard


btnMain = KeyboardButton("Главное меню")

# --- Главное меню ---
btnProfile = KeyboardButton("Мой профиль 🎓")
btninquiry = KeyboardButton("Мое расписание 📅")
btnhelp = KeyboardButton("Инструкция ❓")
btnSettings = KeyboardButton("Настройки ⚙️")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(btnProfile, btninquiry)\
    .add(btnhelp, btnSettings)


# --- Меню настройки ---
btnInfo = KeyboardButton("Сбросить параметры аккаунта 🔄")
btnMoney = KeyboardButton("Вернуться назад 🔙")
settingsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMoney)

# --- Список предметов и часовых поясов(вспомогательное) ---
# НУЖНО ИСПРАВИТЬ ПРЕДМЕТЫ
SubjectsList = [
    "Занимательная лаборатория",
    "Математика Базовый уровень",
    "Физика Базовый уровень",
    "Математика Углубленный уровень",
    "Физика Углубленный уровень",
    "Математика ДФО",
    "Физика ДФО",
    "Основы проектной деятельности",
    "Химия Базовый уровень",
    "Информатика ОГЭ",
    "Русский язык ОГЭ",
    "Химия Углубленный уровень",
    "Информатика ЕГЭ",
    "Русский язык ЕГЭ",
    "Технологические уроки",
    "Математика ЕГЭ",
    "Физика ЕГЭ",
    "Химия ЕГЭ"
]

TimeZonesList = list(map(lambda x: x[0],
                         cursor.execute("SELECT name FROM Timezones")
                         .fetchall()))

classes = list(map(lambda x: x[0],
                   cursor.execute("SELECT name FROM Classes")
                   .fetchall()))

# Создаем кнопки с предметами для каждого класса
buttons = {
    classes[0]: [InlineKeyboardButton(
        SubjectsList[0],
        callback_data=SubjectsList[0])],
    classes[1]: [InlineKeyboardButton(
        SubjectsList[0],
        callback_data=SubjectsList[0])],
    classes[2]: [
        InlineKeyboardButton(SubjectsList[1],
                             callback_data=SubjectsList[1]),
        InlineKeyboardButton(SubjectsList[2],
                             callback_data=SubjectsList[2]),
        InlineKeyboardButton(SubjectsList[3],
                             callback_data=SubjectsList[3]),
        InlineKeyboardButton(SubjectsList[4],
                             callback_data=SubjectsList[4]),
        InlineKeyboardButton(SubjectsList[5],
                             callback_data=SubjectsList[5]),
        InlineKeyboardButton(SubjectsList[6],
                             callback_data=SubjectsList[6]),
        InlineKeyboardButton(SubjectsList[7],
                             callback_data=SubjectsList[7])
        ],
    classes[3]: [
        InlineKeyboardButton(SubjectsList[1],
                             callback_data=SubjectsList[1]),
        InlineKeyboardButton(SubjectsList[2],
                             callback_data=SubjectsList[2]),
        InlineKeyboardButton(SubjectsList[3],
                             callback_data=SubjectsList[3]),
        InlineKeyboardButton(SubjectsList[4],
                             callback_data=SubjectsList[4]),
        InlineKeyboardButton(SubjectsList[5],
                             callback_data=SubjectsList[5]),
        InlineKeyboardButton(SubjectsList[6],
                             callback_data=SubjectsList[6]),
        InlineKeyboardButton(SubjectsList[8],
                             callback_data=SubjectsList[8]),
        InlineKeyboardButton(SubjectsList[9],
                             callback_data=SubjectsList[9]),
        InlineKeyboardButton(SubjectsList[7],
                             callback_data=SubjectsList[7])
    ],
    classes[4]: [
        InlineKeyboardButton(SubjectsList[1],
                             callback_data=SubjectsList[1]),
        InlineKeyboardButton(SubjectsList[2],
                             callback_data=SubjectsList[2]),
        InlineKeyboardButton(SubjectsList[3],
                             callback_data=SubjectsList[3]),
        InlineKeyboardButton(SubjectsList[4],
                             callback_data=SubjectsList[4]),
        InlineKeyboardButton(SubjectsList[5],
                             callback_data=SubjectsList[5]),
        InlineKeyboardButton(SubjectsList[6],
                             callback_data=SubjectsList[6]),
        InlineKeyboardButton(SubjectsList[8],
                             callback_data=SubjectsList[8]),
        InlineKeyboardButton(SubjectsList[9],
                             callback_data=SubjectsList[9]),
        InlineKeyboardButton(SubjectsList[7],
                             callback_data=SubjectsList[7]),
        InlineKeyboardButton(SubjectsList[10],
                             callback_data=SubjectsList[10])
    ],
    classes[5]: [
        InlineKeyboardButton(SubjectsList[3],
                             callback_data=SubjectsList[3]),
        InlineKeyboardButton(SubjectsList[4],
                             callback_data=SubjectsList[4]),
        InlineKeyboardButton(SubjectsList[11],
                             callback_data=SubjectsList[11]),
        InlineKeyboardButton(SubjectsList[12],
                             callback_data=SubjectsList[12]),
        InlineKeyboardButton(SubjectsList[7],
                             callback_data=SubjectsList[7]),
        InlineKeyboardButton(SubjectsList[13],
                             callback_data=SubjectsList[13]),
        InlineKeyboardButton(SubjectsList[14],
                             callback_data=SubjectsList[14])
    ],
    classes[6]: [
        InlineKeyboardButton(SubjectsList[15],
                             callback_data=SubjectsList[15]),
        InlineKeyboardButton(SubjectsList[16],
                             callback_data=SubjectsList[16]),
        InlineKeyboardButton(SubjectsList[17],
                             callback_data=SubjectsList[17]),
        InlineKeyboardButton(SubjectsList[12],
                             callback_data=SubjectsList[12]),
        InlineKeyboardButton(SubjectsList[7],
                             callback_data=SubjectsList[7]),
        InlineKeyboardButton(SubjectsList[13],
                             callback_data=SubjectsList[13]),
        InlineKeyboardButton(SubjectsList[14],
                             callback_data=SubjectsList[14])
    ]
}


# список кнопок с классами и само меню с классами
buttonsClasses = [InlineKeyboardButton(c, callback_data=c)
                  for c in classes]
keyboard = InlineKeyboardMarkup(row_width=1)
for btn in buttonsClasses:
    keyboard.add(btn)

# список кнопок часовых поясов и само меню с часовыми поясами
buttonTimeZones = [InlineKeyboardButton(TZ, callback_data=TZ)
                   for TZ in TimeZonesList]
keyboardTimeZone = InlineKeyboardMarkup(row_width=1)
for btn in buttonTimeZones:
    keyboardTimeZone.add(btn)
