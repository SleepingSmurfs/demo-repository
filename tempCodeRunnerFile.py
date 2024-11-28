logging.basicConfig(level=logging.INFO)
# db_config = {
#     "dbname": "web",  # Замените на имя вашей базы данных
#     "user": "postgres",  # Замените на имя пользователя
#     "password": "toor",  # Замените на пароль пользователя
#     "host": "127.0.0.1",  # Если база данных на локальной машине
#     "port": "5432"  # Обычно стандартный порт PostgreSQL
# }
# def start():
#     conn = psycopg2.connect(
#         dbname="web",
#         user="postgres", 
#         password="toor",  
#         host="127.0.0.1",  
#         port="5432" 
#     )
#     return conn