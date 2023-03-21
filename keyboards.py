from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboards:
    """
    Класс для генерации клавиатур бота
    """

    def __init__(self, db):
        self.db = db

    def get_categories_keyboard(self):
        """
        Получить клавиатуру категорий
        """
        self.db.get_connection()
        cursor = self.db.cursor
        select_categories_sql = """
        SELECT categoryname FROM category
        """
        cursor.execute(select_categories_sql)
        categories = [elem[0] for elem in cursor.fetchall()]
        if not categories:
            return
        keyboard = VkKeyboard(one_time=True)
        self.db.close_connection()
        for index, category in enumerate(categories):
            keyboard.add_button(label=category, color=VkKeyboardColor.PRIMARY)
            if (index + 1) % 3 == 0:
                keyboard.add_line()
        return keyboard.get_keyboard()

    def get_products_keyboard(self, category, chosen_product=None):
        """
        Получить клавиатуру продуктов категории
        """
        self.db.get_connection()
        cursor = self.db.cursor
        get_category_menu_sql = f"""
        SELECT productname FROM product
        JOIN category ON cproductid = categoryid AND categoryname = '{category}'
        ORDER BY productname
        """
        cursor.execute(get_category_menu_sql)
        products = [elem[0] for elem in cursor.fetchall()]
        if not products:
            return
        self.db.close_connection()
        keyboard = VkKeyboard(one_time=True)
        for index, product in enumerate(products):
            if product != chosen_product:
                keyboard.add_button(label=product, color=VkKeyboardColor.PRIMARY)
            else:
                keyboard.add_button(label=product, color=VkKeyboardColor.POSITIVE)
            if (index + 1) % 3 == 0:
                keyboard.add_line()
        keyboard.add_button("Назад к категориям", color=VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        return keyboard
