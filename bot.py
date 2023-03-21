import vk_api
import threading
from fsm import Processing
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Bot:
    """
    Класс, описывающий действия бота
    """
    def __init__(self, token, community_id, db):
        self.token = token
        self.id = community_id
        self.db = db
        self.vk_session = None
        self.vk = None
        self.upload = None
        self.longpoll = None
        self.processing = None

    def run(self):
        """
        Запуск бота
        """
        while True:
            try:
                print("Подключился")
                self.vk_session = vk_api.VkApi(token=self.token)
                self.vk = self.vk_session.get_api()
                self.upload = vk_api.VkUpload(self.vk_session)
                self.longpoll = VkBotLongPoll(self.vk_session, self.id)
                self.processing = Processing(self.vk, self.upload, self.db)
                for event in self.longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                        user_id = event.obj['message']['from_id']
                        message_text = event.obj['message']['text']
                        current_thread = threading.Thread(target=self.processing.processing,
                                                          args=(user_id, message_text))
                        current_thread.name = str(user_id)
                        for thread in threading.enumerate():
                            if current_thread.name == thread.name:
                                raise Exception
                        current_thread.start()
            except Exception as ex:
                print(ex)
