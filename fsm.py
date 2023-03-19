from actions import Actions


class Processing:
    """
    Класс машины состояний
    """

    def __init__(self, vk, upload, db):
        self.vk = vk
        self.upload = upload
        self.db = db

    def processing(self, recieved_user_id, recieved_message_text):
        """
        Выбор действий машины состояний
        :param recieved_user_id:
        :param recieved_message_text:
        :return:
        """
        actions = Actions(received_user_id=recieved_user_id, received_message_text=recieved_message_text,
                          db=self.db, vk=self.vk, upload=self.upload)
        state_number = actions.get_state_number(user_id=recieved_user_id)

        if state_number == actions.NEW_USER:

            actions.send_message(user_id=recieved_user_id,
                                 message_text="Добро пожаловать в Сладкое Королевство!")
            actions.show_categories(user_id=recieved_user_id)
            actions.add_vkuser(recieved_user_id)

        elif state_number == actions.CATEGORIES_STATE:
            actions.show_menu(category=recieved_message_text)

        elif state_number == actions.MENU_STATE:
            actions.show_product(product=recieved_message_text)

        elif state_number == actions.PRODUCT_STATE:
            if recieved_message_text == "Назад к категориям":
                actions.show_categories(user_id=recieved_user_id)
            else:
                actions.show_product(product=recieved_message_text)
