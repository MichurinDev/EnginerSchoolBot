from datetime import timedelta, datetime, date, time
import sqlite3
from modules.markups import *
from modules.SendNotify import send_notify
from modules.config_reader import config
import asyncio
import pytz


def timetable_on_date(date: date, cursor: sqlite3.Cursor):
    """Возвращает множество кортежей
    (название, время начала, время конца, параллель (она-же класс))"""

    return cursor.execute("""SELECT subject, start_time, end_time,
                          class FROM Timetable WHERE date=?""",
                          (date.strftime("%d.%m.%Y"), )).fetchall()


async def mornind_and_evening_notifycations():
    _isSend = False

    while True:
        # moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
        moscow_time = datetime(2023, 10, 28, 9)
        # moscow_time = datetime(2023, 10, 26, 17)

        if moscow_time.time().minute == 0:
            if not _isSend:
                # Подгружаем БД
                conn = sqlite3.connect('res/data/EnginerSchool.db')
                cursor = conn.cursor()

                times = ["09", "17"]

                for tz in TimeZonesList:
                    delta_msk = [int(tz.split()[0][-1])
                                 if tz.split()[0][-2] == "+"
                                 else -int(tz.split()[0][-1])][0]
                    new_time = moscow_time + timedelta(hours=delta_msk)

                    d = new_time.date()
                    t = new_time.time().strftime("%H:%M")
                    hour = t.split(":")[0]

                    if hour in times:
                        users = cursor.execute(f"""SELECT tg_id, class
                                               FROM UsersInfo
                                               WHERE timezone=?""",
                                               (tz,)).fetchall()

                        if users:
                            for user in users:
                                send_text = ""

                                if hour == times[0]:
                                    timetable = timetable_on_date(d, cursor)
                                elif hour == times[1]:
                                    d += timedelta(days=1)
                                    timetable = timetable_on_date(d, cursor)

                                timetable = list(filter(
                                    lambda x: user[1] in x[3], timetable))

                                if timetable:
                                    send_text += "📝 Твоё расписание на " +\
                                        f"{d.strftime('%d.%m.%Y')}:"
                                    for event in timetable:
                                        send_text += f"\n{' ' * 7}" +\
                                            f"•Название: {event[0]}"
                                        send_text += "\nВремя: " +\
                                            f"{event[1]} - {event[2]}\n"

                                    send_notify(TOKEN, send_text, user[0])
                _isSend = True
        else:
            _isSend = False


async def checkSubjects():
    usersGoNotification = []
    spisSubFoNotification = []

    # --- --- Москвоское время + 15 мин---
    time_now = datetime.now(pytz.timezone("Europe/Moscow")) + \
        timedelta(minutes=15)
    date_now = datetime.now(pytz.timezone("Europe/Moscow"))
    time_now_str = time_now.strftime("%H:%M")
    date_now_str = date_now.strftime("%d.%m.20%y")

    for strSubj in cursor.execute("SELECT * FROM Timetable").fetchall():
        if strSubj[2] == date_now_str and strSubj[4] == time_now_str:
            # Наполняем список предметов через 15 минут
            spisSubFoNotification.append([strSubj[0], strSubj[1]])

    for strUsers in cursor.execute("SELECT * FROM UsersInfo").fetchall():
        for subj in spisSubFoNotification:
            if strUsers[3] in subj[1] and subj[0] in strUsers[4]:
                # Наполняем список учеников кому отправлять через 15 минут
                usersGoNotification.append([strUsers[0], subj[0]])

    # Тут лежит список [id, предмет] нужно отправить уведомление
    # данным пользователям о том что у них этот предмет через 15 минут
    for user in usersGoNotification:
        send_text = f"Через 15 минут начаинается урок {user[1]}"
        send_notify(TOKEN, send_text, user[0])


async def checkTime():
    while True:
        # Время сейчас для тестов
        current_time = datetime.now(pytz.timezone("Europe/Moscow")).time()

        # current_time = time(9, 0, 0)

        if current_time.minute == 45:
            await checkSubjects()
        elif current_time.minute == 0:
            await mornind_and_evening_notifycations()
        await asyncio.sleep(60)


async def on_startup():
    asyncio.create_task(checkTime())


TOKEN = config.bot_token.get_secret_value()

if __name__ == '__main__':
    print("Отправитель сообщений запущен...")
    loop = asyncio.get_event_loop()
    loop.create_task(checkTime())
    loop.run_forever()
