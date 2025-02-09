import sqlite3


async def creation():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    # Создаем таблицу Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    birth TEXT,
    name TEXT,
    flag INTEGER
    )
    ''')

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

async def regist_user(user_id):
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    user = cursor.execute(("""SELECT 1 FROM
     Users WHERE id == '{key}'""".format(key=user_id))).fetchone()
    if not user:
        cursor.execute('''
                INSERT INTO Users
                VALUES ( ?, ?, ?,?)
            ''', (user_id,"","",0))
        connection.commit()
        return 0
    return 1


async def giv_data(user_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))

    row = cursor.fetchone()  # Получает одну строку результата
    return row


async def get_data(user_id, data, name):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE Users SET birth = ?, name = ? WHERE id = ?',
                   (data, name, user_id))

    conn.commit()
    conn.close()

import sqlite3

async def newsletter():
    # Подключение к базе данных
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Выполнение запроса
    cursor.execute("SELECT id, flag FROM Users")
    users = cursor.fetchall()

    # Закрытие соединения
    conn.close()

    # Проверка на наличие данных
    if not users:
        return [], []  # Возвращаем пустые списки, если нет результатов

    # Разделяем результаты на два списка
    user_ids = [user[0] for user in users]  # Извлекаем id
    flags = [user[1] for user in users]      # Извлекаем flag
    return user_ids, flags


async def up_flaf(user_id, flag):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE Users SET flag = ? WHERE id = ?',
                   (flag, user_id))

    conn.commit()
    conn.close()