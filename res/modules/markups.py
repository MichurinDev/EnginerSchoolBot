from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3

# Подгружаем БД
conn = sqlite3.connect('res/data/EnginerSchool.db')
cursor = conn.cursor()

# --- Тексты ---
START_TEXT = \
    """
Здравствуйте!
"""

MENU_TEXT = \
    """
Выберите действие:
"""

ACQUAINTANCE_TEXT = \
    """
Давайте познакомимся!
Введите своё ФИО (отчество при его наличии)
"""

HELP_TEXT = \
    """
Инструкция...
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
btninquiry = KeyboardButton("Мое рассписание 📅")
btnSettings = KeyboardButton("Настройки ⚙️")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(btnProfile, btninquiry)\
    .add(btnSettings)


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
    classes[2]: [InlineKeyboardButton(
        SubjectsList[0],
        callback_data=SubjectsList[0])],
    classes[3]: [InlineKeyboardButton(
        SubjectsList[0],
        callback_data=SubjectsList[0])],
    classes[4]: [InlineKeyboardButton(
        SubjectsList[0],
        callback_data=SubjectsList[0])],
    classes[5]: [InlineKeyboardButton(
        SubjectsList[0],
        callback_data=SubjectsList[0])],

    classes[6]: [
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
    classes[7]: [
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
    classes[8]: [
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
    classes[9]: [
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
    classes[10]: [
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
