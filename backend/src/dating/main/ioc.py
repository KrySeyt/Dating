from contextlib import contextmanager
from typing import Generator

from dating.adapters.database.ram_user_db import RAMUserGateway
from dating.application.chat.create_chat import CreateChat
from dating.application.chat.delete_chat import DeleteChat
from dating.application.chat.get_chat import GetChat
from dating.application.user.create_user import CreateUser
from dating.application.user.get_user import GetUser
from dating.domain.services.chat import ChatService
from dating.domain.services.user import UserService
from dating.presentation.interactor_factory.chat import ChatInteractorFactory
from dating.adapters.database.ram_chat_db import RAMChatGateway
from dating.presentation.interactor_factory.user import UserInteractorFactory


class ChatIoC(ChatInteractorFactory):
    def __init__(self) -> None:
        self._chat_gateway = RAMChatGateway()

    @contextmanager
    def get_chat(self) -> Generator[GetChat, None, None]:
        yield GetChat(self._chat_gateway)

    @contextmanager
    def create_chat(self) -> Generator[CreateChat, None, None]:
        yield CreateChat(ChatService(), self._chat_gateway)

    @contextmanager
    def delete_chat(self) -> Generator[DeleteChat, None, None]:
        yield DeleteChat(self._chat_gateway)


class UserIoC(UserInteractorFactory):
    def __init__(self) -> None:
        self._user_gateway = RAMUserGateway()

    @contextmanager
    def get_user(self) -> Generator[GetUser, None, None]:
        yield GetUser(
            UserService(),
            self._user_gateway
        )

    @contextmanager
    def create_user(self) -> Generator[CreateUser, None, None]:
        yield CreateUser(
            UserService(),
            self._user_gateway
        )
