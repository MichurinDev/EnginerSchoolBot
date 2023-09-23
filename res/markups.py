from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup


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
SubjectsList = [
    "Занимательная лаборатория",
    "математика база",
    "физика база",
    "математика углубленный",
    "физика углубленный",
    "математика Дальний Восток",
    "физика Дальний Восток",
    "Основы проектной деятельности",
    "химия база",
    "Информатика ОГЭ",
    "Русский язык ОГЭ",
    "химия углубленный",
    "Информатика ЕГЭ",
    "Русский язык ЕГЭ",
    "Технологические уроки",
    "математика ЕГЭ",
    "физика ЕГЭ",
    "химия ЕГЭ"
]

TimeZonesList = [
    "МСК-1(Калининградское)",
    "МСК(Московское)",
    "МСК+1(Самарское)",
    "МСК+2(Екатеринбургское)",
    "МСК+3(Омское)",
    "МСК+4(Красноярское)",
    "МСК+5(Иркутское)",
    "МСК+6(Якутское)",
    "МСК+7(Владивостокское)",
    "МСК+8(Магаданское)",
    "МСК+9(Камчатское)",
]

# Создаем кнопки с предметами для каждого класса
buttons = {
    "1-4Class": [InlineKeyboardButton(
        "Занимательная лаборатория",
        callback_data="Занимательная лаборатория")],
    "5-6Class": [InlineKeyboardButton(
        "Занимательная лаборатория",
        callback_data="Занимательная лаборатория")],
    "7Class": [
        InlineKeyboardButton("математика база",
                             callback_data="математика база"),
        InlineKeyboardButton("физика база",
                             callback_data="физика база"),
        InlineKeyboardButton("математика углубленный",
                             callback_data="математика углубленный"),
        InlineKeyboardButton("физика углубленный",
                             callback_data="физика углубленный"),
        InlineKeyboardButton("математика Дальний Восток",
                             callback_data="математика Дальний Восток"),
        InlineKeyboardButton("физика Дальний Восток",
                             callback_data="физика Дальний Восток"),
        InlineKeyboardButton("Основы проектной деятельности",
                             callback_data="Основы проектной деятельности"),
        InlineKeyboardButton("Основы проектной деятельности",
                             callback_data="Основы проектной деятельности")
        ],
    "8Class": [
        InlineKeyboardButton("математика база",
                             callback_data="математика база"),
        InlineKeyboardButton("физика база",
                             callback_data="физика база"),
        InlineKeyboardButton("математика углубленный",
                             callback_data="математика углубленный"),
        InlineKeyboardButton("физика углубленный",
                             callback_data="физика углубленный"),
        InlineKeyboardButton("математика Дальний Восток",
                             callback_data="математика Дальний Восток"),
        InlineKeyboardButton("физика Дальний Восток",
                             callback_data="физика Дальний Восток"),
        InlineKeyboardButton("химия база",
                             callback_data="химия база"),
        InlineKeyboardButton("Информатика ОГЭ",
                             callback_data="Информатика ОГЭ"),
        InlineKeyboardButton("Основы проектной деятельности",
                             callback_data="Основы проектной деятельности")
    ],
    "9Class": [
        InlineKeyboardButton("математика база",
                             callback_data="математика база"),
        InlineKeyboardButton("физика база",
                             callback_data="физика база"),
        InlineKeyboardButton("математика углубленный",
                             callback_data="математика углубленный"),
        InlineKeyboardButton("физика углубленный",
                             callback_data="физика углубленный"),
        InlineKeyboardButton("математика Дальний Восток",
                             callback_data="математика Дальний Восток"),
        InlineKeyboardButton("физика Дальний Восток",
                             callback_data="физика Дальний Восток"),
        InlineKeyboardButton("химия база",
                             callback_data="химия база"),
        InlineKeyboardButton("Информатика ОГЭ",
                             callback_data="Информатика ОГЭ"),
        InlineKeyboardButton("Основы проектной деятельности",
                             callback_data="Основы проектной деятельности"),
        InlineKeyboardButton("Русский язык ОГЭ",
                             callback_data="Русский язык ОГЭ")
    ],
    "10Class": [
        InlineKeyboardButton("математика углубленный",
                             callback_data="математика углубленный"),
        InlineKeyboardButton("физика углубленный",
                             callback_data="физика углубленный"),
        InlineKeyboardButton("химия углубленный",
                             callback_data="химия углубленный"),
        InlineKeyboardButton("Информатика ЕГЭ",
                             callback_data="Информатика ЕГЭ"),
        InlineKeyboardButton("Основы проектной деятельности",
                             callback_data="Основы проектной деятельности"),
        InlineKeyboardButton("Русский язык ЕГЭ",
                             callback_data="Русский язык ЕГЭ"),
        InlineKeyboardButton("Технологические уроки",
                             callback_data="Технологические уроки")
    ],
    "11Class": [
        InlineKeyboardButton("математика ЕГЭ",
                             callback_data="математика ЕГЭ"),
        InlineKeyboardButton("физика ЕГЭ",
                             callback_data="физика ЕГЭ"),
        InlineKeyboardButton("химия ЕГЭ",
                             callback_data="химия ЕГЭ"),
        InlineKeyboardButton("Информатика ЕГЭ",
                             callback_data="Информатика ЕГЭ"),
        InlineKeyboardButton("Основы проектной деятельности",
                             callback_data="Основы проектной деятельности"),
        InlineKeyboardButton("Русский язык ЕГЭ",
                             callback_data="Русский язык ЕГЭ"),
        InlineKeyboardButton("Технологические уроки",
                             callback_data="Технологические уроки")
    ]
}


# список кнопок с классами и само меню с классами
buttonsClasses = [
    InlineKeyboardButton("1-4 класс", callback_data="1-4Class"),
    InlineKeyboardButton("5-6 класс", callback_data="5-6Class"),
    InlineKeyboardButton("7 класс", callback_data="7Class"),
    InlineKeyboardButton("8 класс", callback_data="8Class"),
    InlineKeyboardButton("9 класс", callback_data="9Class"),
    InlineKeyboardButton("10 класс", callback_data="10Class"),
    InlineKeyboardButton("11 класс", callback_data="11Class")
]

buttonsClasses = [buttonsClasses[i:i + 2]
                  for i in range(0, len(buttonsClasses), 2)]
keyboard = InlineKeyboardMarkup(row_width=1)
for row in buttonsClasses:
    keyboard.add(*row)

# список кнопок часовых поясов и само меню с часовыми поясами
buttonTimeZones = [InlineKeyboardButton(TZ, callback_data=TZ)
                   for TZ in TimeZonesList]
buttonTimeZones = [buttonTimeZones[i:i + 2]
                   for i in range(0, len(buttonTimeZones), 2)]
keyboardTimeZone = InlineKeyboardMarkup(row_width=1)

for row in buttonTimeZones:
    keyboardTimeZone.add(*row)
