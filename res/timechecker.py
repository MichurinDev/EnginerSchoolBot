from datetime import timedelta, datetime, date, time
import sqlite3
from modules.markups import *
from modules.SendNotify import send_notify
from modules.config_reader import config
import asyncio
import pytz


def timetable_on_date(date: date, cursor: sqlite3.Cursor):
    """Возвращает множество кортежей
    (название, время начала, время конца, параллель (она-же класс))
    По дате"""

    return cursor.execute("""SELECT subject, start_time, end_time,
                          class FROM Timetable WHERE date=?""",
                          (date.strftime("%d.%m.%Y"), )).fetchall()


async def mornind_and_evening_notifycations(moscow_time: datetime):
    # Часы утренних и вечерних уведомлений
    times = ["10", "19"]

    # Перебираем часовые пояса
    for tz in TimeZonesList:
        # Берем разницу времени с Мск
        delta_msk = [int(tz.split()[0][-2:])][0]

        # Получаем актуальное время в часовом поясе tz
        new_time = moscow_time + timedelta(hours=delta_msk)

        # Получаем из datetime -> date, time
        d = new_time.date()
        t = new_time.time().strftime("%H:%M")

        # Извлекаем кол-во часов
        hour = t.split(":")[0]

        # Если это время входит в утреннюю или вечернюю рассылку
        if hour in times:
            # Берем всех пользователей с этим часовыым поясом
            users = cursor.execute(f"""SELECT tg_id, class, subjects
                                   FROM UsersInfo
                                   WHERE timezone=? AND type="Ученик" """,
                                   (tz,)).fetchall()
            # Если такие есть
            if users:
                # Перебираем пользователей
                for user in users:
                    send_text = ""

                    # Поучаем расписание
                    if hour == times[0]:
                        timetable = timetable_on_date(d, cursor)
                        send_text = "Доброе утро ☀️\nУ тебя сегодня:"
                    elif hour == times[1]:
                        d += timedelta(days=1)
                        timetable = timetable_on_date(d, cursor)
                        send_text = "Добрый вечер 🤗\n" +\
                            "Не забудь что завтра у тебя:"

                    if timetable:
                        # Перебираем расписание
                        for e in timetable:
                            # Если класс пользователя находится в приглашенных
                            # и название урокак находится
                            # в указанных пользователем
                            if user[1] in e[3] and e[0] in user[2]:
                                time_start = \
                                    (datetime.strptime(e[1], "%H:%M") +
                                     timedelta(hours=delta_msk))\
                                    .strftime("%H:%M")
                                time_end = \
                                    (datetime.strptime(e[2], "%H:%M") +
                                     timedelta(hours=delta_msk))\
                                    .strftime("%H:%M")

                                # Формируем текст для отправки
                                send_text += f"\n{' ' * 7}" +\
                                    f"• {e[0]}"
                                send_text += f"\n{' ' * 10}Время: " +\
                                    f"{time_start} - {time_end}\n"

                        # Дописываем конец предложения
                        if hour == times[0]:
                            send_text += "\nПродуктивного дня 🎯"
                        elif hour == times[1]:
                            send_text += "\nХорошего отдыха 🌙"

                        # Отправляем сообщение
                        send_notify(TOKEN, send_text, user[0])


async def checkSubjects(moscow_datetime: datetime):
    SubjListForNotification = []

    # --- --- Москвоское время + 15 мин---
    date_now = moscow_datetime.strftime("%d.%m.%Y")
    time_now = (moscow_datetime + timedelta(minutes=15)).strftime("%H:%M")

    # Уроки, которые начинаются в это время
    SubjListForNotification = cursor.execute("""SELECT subject, class
                                             FROM Timetable WHERE date=?
                                             AND start_time=?""",
                                             (date_now, time_now)).fetchall()
    users = cursor.execute("""SELECT tg_id, subjects,
                           class FROM UsersInfo WHERE
                           type="Ученик" """).fetchall()
    if users:
        # Перебираем всех пользователей
        for user in users:
            # Перебираем все полученные предметы
            for subj in SubjListForNotification:
                # Если пользователь зарегистрирован на урок
                # и его класс приглешен
                if subj[0] in user[1] and user[2] in subj[1]:
                    # Отправляем уведомление
                    send_text = "Не забудь что через 15 минут у тебя " +\
                                    f"начинается занятие 👨‍🏫\n\n" +\
                                    f"• {subj[0]}\n" +\
                                    "\nПродуктивной учебы 💯"
                    send_notify(TOKEN, send_text, user[0])


async def checkTime():
    while True:
        # Время сейчас для тестов
        current_time = datetime.now(pytz.timezone("Europe/Moscow"))
        # current_time = datetime(2023, 10, 1, 10, 00)
        # current_time = datetime(2023, 10, 10, 13, 45)

        if current_time.minute == 45:
            await checkSubjects(current_time)
        elif current_time.minute == 0:
            await mornind_and_evening_notifycations(current_time)
        await asyncio.sleep(15 * 60)


async def on_startup():
    asyncio.create_task(checkTime())


# Токен клиентского бота
TOKEN = config.bot_token.get_secret_value()

# Подгружаем БД
conn = sqlite3.connect('res/data/EnginerSchool.db')
cursor = conn.cursor()

if __name__ == '__main__':
    print("Отправитель сообщений запущен...")
    loop = asyncio.get_event_loop()
    loop.create_task(checkTime())
    loop.run_forever()
