from abc import ABC, abstractmethod
from typing import ContextManager

from dating.application.chat.create_chat import CreateChat
from dating.application.chat.delete_chat import DeleteChat
from dating.application.chat.get_chat import GetChat


class ChatInteractorFactory(ABC):
    @abstractmethod
    def get_chat(self) -> ContextManager[GetChat]:
        raise NotImplementedError

    @abstractmethod
    def create_chat(self) -> ContextManager[CreateChat]:
        raise NotImplementedError

    @abstractmethod
    def delete_chat(self) -> ContextManager[DeleteChat]:
        raise NotImplementedError
