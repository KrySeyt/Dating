from abc import ABC, abstractmethod

from dating.domain.models.chat import Chat


class ChatGateway(ABC):
    @abstractmethod
    def save_chat(self, chat: Chat) -> Chat:
        raise NotImplementedError
