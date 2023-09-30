from datetime import datetime, timedelta
import asyncio
import pytz
import sqlite3


# Подключаем БД
conn = sqlite3.connect('res/data/EnginerSchool.db')
cursor = conn.cursor()

async def checkSubjects():
    usersGoNotification = []
    spisSubFoNotification = []

    # --- --- Москвоское время + 15 мин--- 
    time_now = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(minutes=15)
    date_now = datetime.now(pytz.timezone("Europe/Moscow"))
    time_now_str = time_now.strftime("%H:%M")
    date_now_str = date_now.strftime("%d.%m.20%y")
    
    for strSubj in cursor.execute("SELECT * FROM Timetable").fetchall():
        if strSubj[2] == date_now_str and strSubj[4] == time_now_str:
            spisSubFoNotification.append([strSubj[0], strSubj[1]]) #наполняем список предметов через 15 минут
    
    for strUsers in cursor.execute("SELECT * FROM UsersInfo").fetchall():
        for subj in spisSubFoNotification:
            if strUsers[3] in subj[1] and subj[0] in strUsers[4]:
                usersGoNotification.append([strUsers[0], subj[0]]) #наполняем список учеников кому отправлять через 15 минут
                
    print(usersGoNotification) # Тут лежит список [id, предмет] нужно отправить уведомление данным пользователям о том что у них этот предмет через 15 минут

async def checkTime():
    while True:
        current_time = datetime.now(pytz.timezone("Europe/Moscow")).time() # Время сейчас для тестов
        if current_time.minute == 45:
            await checkSubjects()
        await asyncio.sleep(60)
        
async def on_startup(): 
    asyncio.create_task(checkTime())

if __name__ == '__main__':
    print("Отправитель сообщений запущен...")
    loop = asyncio.get_event_loop()
    loop.create_task(checkTime())
    loop.run_forever()

