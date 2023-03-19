from database import Database
from bot import Bot
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("ACCESS_TOKEN")
community_id = os.getenv("COMMUNITY_ID")
database_password = os.getenv("POSTGRES_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("POSTGRES_USER")
if not all([token, community_id, database_name, database_password, database_user]):
    print("""
    Для корректного запуска программы требуется добавить в корневой каталог проекта файл '.env'
    и добавить в него константы:
    ACCESS_TOKEN = "<Токен сообщества>"
    COMMUNITY_ID = "<ID сообщества>"
    POSTGRES_USER = "<Пользователь базы данных>"
    POSTGRES_PASSWORD = "<Пароль к базе данных>"
    DATABASE_NAME = "<Имя базы данных>"
    """)
    exit()

db = Database(database_name, database_user, database_password)

if __name__ == '__main__':
    bot = Bot(token, community_id, db)
    bot.run()
