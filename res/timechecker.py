from datetime import timedelta, datetime, date
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


async def mornind_and_evening_notifycations(moscow_time: datetime):
    # Часы утренних и вечерних уведомлений
    times = ["09", "17"]

    # Перебираем часовые пояса
    for tz in TimeZonesList:
        # Берем разницу времени с Мск
        delta_msk = [int(tz.split()[0][-2])][0]

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
            users = cursor.execute(f"""SELECT tg_id, class
                                   FROM UsersInfo
                                   WHERE timezone=?""",
                                   (tz,)).fetchall()

            # Если такие есть
            if users:
                # Перебираем пользователей
                for user in users:
                    send_text = ""

                    # Поучаем расписание
                    if hour == times[0]:
                        timetable = timetable_on_date(d, cursor)
                    elif hour == times[1]:
                        d += timedelta(days=1)
                        timetable = timetable_on_date(d, cursor)

                    # Берем только те уроки,
                    # на которые зарегистрирован пользователь
                    timetable = list(filter(
                        lambda x: user[1] in x[3], timetable))

                    # Если такие уроки есть
                    if timetable:
                        # Формируем текст для отправки
                        send_text += "📝 Твоё расписание на " +\
                            f"{d.strftime('%d.%m.%Y')}:"

                        for event in timetable:
                            send_text += f"\n{' ' * 7}" +\
                                f"•Название: {event[0]}"
                            send_text += "\nВремя: " +\
                                f"{event[1]} - {event[2]}\n"

                        # Отправляем сообщение
                        send_notify(TOKEN, send_text, user[0])
                        print("Отправка")


async def checkSubjects():
    SubjListForNotification = []

    # --- --- Москвоское время + 15 мин---
    time_now = datetime.now(pytz.timezone("Europe/Moscow")) + \
        timedelta(minutes=15).strftime("%H:%M")

    # Уроки, которые начинаются в это время
    SubjListForNotification = \
        list(map(lambda x: x[0],
                 cursor.execute("""SELECT subject
                                FROM Timetable WHERE start_time=?""",
                                (time_now,)).fetchall()))

    # Перебираем всех пользователей
    for user in cursor.execute("SELECT tg_id, subjects FROM UsersInfo")\
            .fetchall():
        # Перебираем все полученные предметы
        for subj in SubjListForNotification:
            # Если пользователь зарегистрирован на урок
            if subj in user[1]:
                # Отправляем уведомление
                send_text = f"Через 15 минут начинается урок {user[1]}"
                send_notify(TOKEN, send_text, user[0])


async def checkTime():
    while True:
        # Время сейчас для тестов
        current_time = datetime.now(pytz.timezone("Europe/Moscow")).time()
        # current_time = time(9, 0, 0)

        if current_time.minute == 45:
            await checkSubjects()
        elif current_time.minute == 0:
            await mornind_and_evening_notifycations(current_time)
        await asyncio.sleep(60)


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
