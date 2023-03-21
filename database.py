import psycopg2


class Database:
    """
    Класс для работы с базой данных PostgreSQL
    """

    def __init__(self, db_name, user, password):
        self.cursor = None
        self.connection = None
        self.db_name = db_name
        self.password = password
        self.user = user
        self.create_data_base()

    def get_connection(self, db_exists=True):
        """
        Подключиться к базе данных
        """
        try:
            kwargs = {"user": self.user,
                      "password": self.password,
                      "host": "candy_db",
                      "port": "5444"}
            if db_exists:
                kwargs["database"] = self.db_name
            self.connection = psycopg2.connect(**kwargs)
            self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()
        except Exception as ex:
            print(ex)
            print("Проверьте настройки PostgreSQL")
            exit()

    def create_data_base(self):
        """
        Создание базы данных
        """
        try:
            self.get_connection(db_exists=False)
            self.cursor.execute(f"CREATE DATABASE {self.db_name}")
            self.close_connection()
            self.get_connection()
            create_category_table_sql = """
            CREATE TABLE category (
            categoryid SERIAL PRIMARY KEY,
            categoryname VARCHAR(30)
            );
            """
            create_product_table_sql = """
            CREATE TABLE product (
            productid SERIAL PRIMARY KEY,
            productname VARCHAR(30),
            productdescription VARCHAR(255),
            productimgpath VARCHAR(255),
            cproductid INTEGER NOT NULL REFERENCES category
            );
            """
            create_vkuser_table_sql = """
            CREATE TABLE vkuser (
            vkuserid INTEGER PRIMARY KEY,
            state INTEGER
            );
            """
            self.cursor.execute(create_category_table_sql)
            self.cursor.execute(create_product_table_sql)
            self.cursor.execute(create_vkuser_table_sql)
            print(f"Создана и настроена новая база данных: {self.db_name}")
        except Exception:
            print("Ошибка в PostgreSQL или база данных уже существует")

    def close_connection(self):
        """
        Закрытие подключения
        """
        if self.cursor:
            self.cursor.close()
            self.connection.close()
