from datetime import timedelta, datetime, date
import sqlite3
from modules.markups import *
from modules.SendNotify import send_notify
from modules.config_reader import config


def timetable_on_date(date: date, cursor: sqlite3.Cursor):
    return cursor.execute("""SELECT subject, start_time, end_time,
                          class FROM Timetable WHERE date=?""",
                          (date.strftime("%d.%m.%Y"), )).fetchall()


print("Timechecker runned...")

TOKEN = config.bot_token.get_secret_value()
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

                            timetable = list(filter(lambda x: user[1] in x[3],
                                                    timetable))

                            if timetable:
                                send_text += \
                                    f"Расписание на {d.strftime('%d.%m.%Y')}:"
                                for event in timetable:
                                    send_text += f"\nНазвание: {event[0]}"
                                    send_text += \
                                        f"\nВремя: {event[1]} - {event[2]}\n"

                                send_notify(TOKEN, send_text, user[0])
            _isSend = True
    else:
        _isSend = False
