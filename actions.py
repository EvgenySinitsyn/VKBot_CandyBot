from vk_api.utils import get_random_id
from keyboards import Keyboards
import os


class Actions:
    """
    Класс, включающий в себя действия бота
    """
    NEW_USER = 0
    CATEGORIES_STATE = 1
    MENU_STATE = 2
    PRODUCT_STATE = 3
    BACK_TO_CATEGORIES_BUTTON = "Назад к категориям"

    def __init__(self, received_user_id, received_message_text, db, vk, upload):
        self.received_user_id = received_user_id
        self.received_message_text = received_message_text
        self.db = db
        self.vk = vk
        self.upload = upload

    def send_message(self, user_id, message_text, keyboard=None, attachment=None):
        """
        Отправить сообщение
        """
        try:
            kwargs = {
                "user_id": user_id,
                "random_id": get_random_id(),
                "keyboard": keyboard,
                "message": message_text
            }
            if attachment:
                kwargs["attachment"] = attachment
            self.vk.messages.send(**kwargs)
        except Exception as ex:
            print(ex)

    def set_user_state(self, state):
        """
        Обновить состояние пользователя
        """
        self.db.get_connection()
        cursor = self.db.cursor
        set_vkuser_state_sql = f"""
            UPDATE vkuser
            SET state = {state}
            WHERE vkuserid = {self.received_user_id};
            """
        cursor.execute(set_vkuser_state_sql)

    def show_menu(self, category):
        """
        Показать меню товаров категории
        """
        self.set_user_state(self.MENU_STATE)
        keyboard = Keyboards(self.db).get_products_keyboard(category)
        if keyboard:
            self.send_message(user_id=self.received_user_id, message_text="Выберите наименование товара: ", keyboard=keyboard)
        else:
            self.send_message(user_id=self.received_user_id, message_text='Неизвестная команда...')
            self.show_categories()

    def show_product(self, product):
        """
        Показать детализацию продукта
        """
        try:
            self.db.get_connection()
            cursor = self.db.cursor
            get_product_sql = f"""
            SELECT productname, productdescription, productimgpath FROM product
            WHERE productname = '{product}'
            """
            self.set_user_state(self.PRODUCT_STATE)
            cursor.execute(get_product_sql)
            chosen_product = cursor.fetchone()
            root = os.path.dirname(os.path.abspath(__file__))
            photo = self.upload.photo_messages(root + chosen_product[2])
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            get_category_sql = f"""
            SELECT categoryname FROM category
            JOIN product ON productname = '{product}' AND cproductid = categoryid;
            """
            cursor.execute(get_category_sql)
            category = cursor.fetchone()[0]
            keyboard = Keyboards(self.db).get_products_keyboard(category=category, chosen_product=product)
            self.send_message(user_id=self.received_user_id, message_text=chosen_product[1], keyboard=keyboard,
                              attachment=attachment)
            self.db.close_connection()
        except:
            if product != self.BACK_TO_CATEGORIES_BUTTON:
                self.send_message(user_id=self.received_user_id, message_text='Неизвестная команда...')
            self.show_categories()
            self.db.close_connection()

    def show_categories(self):
        """
        Показать категории
        """
        self.db.get_connection()
        cursor = self.db.cursor
        self.set_user_state(self.CATEGORIES_STATE)
        self.db.close_connection()
        keyboard = Keyboards(self.db).get_categories_keyboard()
        if keyboard:
            self.send_message(user_id=self.received_user_id, message_text="Выберите категорию: ", keyboard=keyboard)
        else:
            self.send_message(user_id=self.received_user_id, message_text="Магазин пуст...")

    def get_state_number(self, user_id):
        """
        Получить состояние пользователя
        """
        try:
            self.db.get_connection()
            cursor = self.db.cursor
            get_state_sql = f"""
            SELECT state FROM vkuser
            WHERE vkuserid = {user_id}
            """
            cursor.execute(get_state_sql)
            state = cursor.fetchone()[0]
            self.db.close_connection()
            return state
        except:
            self.db.close_connection()
            return self.NEW_USER

    def add_vkuser(self, id_user):
        """
        Добавить нового пользователя в БД
        """
        self.db.get_connection()
        cursor = self.db.cursor
        add_vkuser_sql = f"""
            INSERT INTO vkuser (vkuserid, state) VALUES ({id_user}, 1)
        """
        cursor.execute(add_vkuser_sql)
        self.db.close_connection()
