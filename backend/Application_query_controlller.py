import psycopg2
import os
from psycopg2 import sql
import logging

# Настройки логирования (для отладки)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Настройки из переменных окружения
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "mydatabase")
DB_USER = os.environ.get("DB_USER", "myuser")
DB_PASS = os.environ.get("DB_PASS", "mypassword")
FETCH_SIZE = int(os.environ.get("FETCH_SIZE", 1000)) # Настраиваемый fetch_size


def execute_query(query, params=None):
    """Выполняет SQL-запрос с расширенной оптимизацией."""
    conn = None
    cur = None
    results = []
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        conn.autocommit = True # Автокоммит для повышения производительности (с осторожностью!)

        cur = conn.cursor("mycursor")
        cur.itersize = FETCH_SIZE # itersize для fetchmany
        cur.execute(query, params or ())

        for record in cur: # Итератор для экономии памяти
            results.append(record)

        logging.info(f"Запрос выполнен успешно. Найдено {len(results)} записей.")

    except psycopg2.Error as e:
        logging.error(f"Ошибка БД: {e}")
        if conn:
            conn.rollback()
    except Exception as e: # Обработка других исключений
        logging.exception(f"Произошла непредвиденная ошибка: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return results

# Пример использования:
#  ОБЯЗАТЕЛЬНО создайте индексы на используемых полях!

# Получение данных по частям (только необходимые поля)
users = execute_query("SELECT id, username FROM users")
if users:
    for user in users:
        print(user)

# Запрос с параметрами (безопасный с psycopg2.sql)
user_id = 1
user = execute_query(sql.SQL("SELECT id, username FROM users WHERE id = {}").format(sql.Placeholder("user_id")), {"user_id": user_id})
if user:
    print(user)

#Пример запроса с ограничением и сортировкой (для больших данных)
limit = 1000
offset = 0
users_paginated = execute_query(sql.SQL("SELECT id, username FROM users ORDER BY id LIMIT {} OFFSET {}").format(sql.Literal(limit), sql.Literal(offset)))
if users_paginated:
    for user in users_paginated:
      print(user)