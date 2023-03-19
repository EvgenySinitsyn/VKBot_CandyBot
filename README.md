# Чат-бот Вконтакте

### Сервис предоставляет меню кондитерской

## Запуск<br/>
    1. Скачать репозиторий в свое окружение
    2. Запустить команду docker-compose up --build
    3. Создать сообщество VK, настроить Работу с API и LongPoll на прием собщений
    4. Получить Токен и ID сообщества
    5. Для корректного запуска программы требуется добавить в корневой каталог 
    проекта файл '.env' и добавить в него константы:
    ACCESS_TOKEN = "<Токен сообщества>"
    COMMUNITY_ID = "<ID сообщества>"
    POSTGRES_USER = "<Пользователь базы данных>"
    POSTGRES_PASSWORD = "<Пароль к базе данных>"
    DATABASE_NAME = "<Имя базы данных>"

## База данных

### 1. Таблица category
Содержит категории товаров
#### Поля:
1. categoryid INTEGER
2. categoryname VARCHAR(30) - наименование категории

### 2. Таблица product
Содержит данные о товарах
#### Поля:
1. productid INTEGER
2. productname VARCHAR(30) - наименование товара
3. productdescription VARCHAR(255) -  описание товара
4. productimgpath VARCHAR(255) - путь к изображению товара
    относительно корневого каталога проекта
5. cproductid INTEGER - ссылка на категорию товара

### 3. Таблица vkuser
Содержит данные о пользователях бота
#### Поля:
1. vkuserid INTEGER
2. state INTEGER - текущее состояние пользователя в боте


