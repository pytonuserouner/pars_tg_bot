import sqlite3


def create_table():
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS level(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    age INT, 
    min_count INT,
    max_count INT,
    scary INT,
    rating FLOAT,
    type TEXT,
    status TEXT,
    url TEXT UNIQUE NOT NULL
    );
    """)
    connection.commit()
    connection.close()


# def push_data(age, count, scary, rating, typs, status, url):
#     connection = sqlite3.connect("data.sqlite3")
#     cursor = connection.cursor()
#     cursor.execute(
#             """INSERT INTO scrapy (age, count, scary, rating, type, status, url) VALUES (?, ?, ?, ?, ?, ?, ?)""",
#             (age, count, scary, rating, typs, status, url)
#     )
#     connection.commit()
#     connection.close()


def new_push_data(data_list: list) -> None:
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    for i in data_list:
        cursor.execute(
            """INSERT INTO level (age, min_count, max_count, scary, rating, type, status, url) VALUES (?, ?, ?, ?, ?, 
            ?, ?, ?)""",
            (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        )
    connection.commit()
    connection.close()


# def read_data(rez_list) -> list:
#     """
#         Принимает id пользователя, делает запрос к базе данных, получает в ответ
#         результаты запросов данного пользователя.
#         : param user : int
#         : return : list
#     """
#     connection = sqlite3.connect("data.sqlite3")
#     cursor = connection.cursor()
#     cursor.execute(
#         "SELECT url FROM scrapy WHERE age >= ? AND count <=? "
#         "AND scary >= ? AND rating >= ? AND type = ?", (rez_list[0], rez_list[1], rez_list[2], rez_list[3], rez_list[4]))
#     records = cursor.fetchall()
#     connection.close()
#     return records


def read_data_age(age_num: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
        """SELECT OID FROM level WHERE age >= ?""", [age_num])
    records_age = cursor.fetchall()
    connection.close()
    return records_age


def read_data_members(records_age: list, min_mem: int, max_mem: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    records_members = []
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
            """SELECT OID FROM level WHERE min_count >= ? AND max_count <= ?""", (min_mem, max_mem))
    records = cursor.fetchall()
    connection.close()
    for i in records:
        if i in list(records_age):
            records_members.append(i)
    return records_members


def read_data_scary(records_members: list, scary: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    records_scary = []
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
            """SELECT OID FROM level WHERE scary >= ?""", [scary])
    records = cursor.fetchall()
    connection.close()
    for i in records:
        if i in list(records_members):
            records_scary.append(i)
    return records_scary


def read_data_rating(records_scary: list, rating: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    records_rating = []
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
            """SELECT OID FROM level WHERE rating >= ?""", [rating])
    records = cursor.fetchall()
    connection.close()
    for i in records:
        if i in list(records_scary):
            records_rating.append(i)
    return records_rating


def read_data_type(records_rating: list, types: str) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    records_type = []
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
            """SELECT OID FROM level WHERE type == ?""", (types,))
    records = cursor.fetchall()
    connection.close()
    for i in records:
        if i in list(records_rating):
            records_type.append(i)
    return records_type


def get_url_query(number_id: int) -> list:
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
        """SELECT url FROM level WHERE OID = ? """, [number_id])
    records = cursor.fetchall()
    connection.close()
    return list(records)



# def sort_data_age(volume) -> list:
#     """
#     Принимает значение колонки age таблицы для сортировки,
#     делает запрос к базе данных, получает ответ в виде списка id значений таблицы,
#     подходящих под запрос пользователя
#     :param volume: int
#     :return: list
#     """
#     connection = sqlite3.connect("data.sqlite3")
#     cursor = connection.cursor()
#     cursor.execute(
#         "SELECT 'id' FROM scrapy WHERE age <= ?", volume)
#     records = cursor.fetchall()
#     connection.close()
#     return records
