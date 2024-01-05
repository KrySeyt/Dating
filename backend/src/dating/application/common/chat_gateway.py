from abc import ABC, abstractmethod

from dating.domain.models.chat import Chat, ChatId


class ChatGateway(ABC):
    @abstractmethod
    def save_chat(self, chat: Chat) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def get_chat_by_id(self, id_: ChatId) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def delete_chat_by_id(self, id_: ChatId) -> Chat:
        raise NotImplementedError
