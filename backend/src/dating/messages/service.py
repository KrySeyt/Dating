from abc import ABC, abstractmethod
from typing import Generator, Callable

from .schema import Message, MessageIn
from .crud import RAMMessageCrud
from ..chats.service import ChatService, ChatServiceFactory
from ..chats.exceptions import UserNotInChat, ChatDoesntExist


class MessageServiceImp(ABC):
    @abstractmethod
    def get_by_id(self, chat_id: int) -> Message | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_messages(self, user_id: int) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    def create(self, message_in: MessageIn, owner_id: int) -> Message:
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, message_id: int) -> Message | None:
        raise NotImplementedError


class RAMMessageServiceImp(MessageServiceImp):
    def __init__(self, crud: RAMMessageCrud) -> None:
        self.db = crud

    def get_by_id(self, chat_id: int) -> Message | None:
        return self.db.get_by_id(chat_id)

    def get_user_messages(self, user_id: int) -> list[Message]:
        return self.db.get_user_messages(user_id)

    def create(self, message_in: MessageIn, owner_id: int) -> Message:
        return self.db.create(message_in, owner_id)

    def delete_message(self, message_id: int) -> Message | None:
        return self.db.delete(message_id)


class MessageService:
    def __init__(self, implementation: MessageServiceImp, chat_service: ChatService) -> None:
        self.imp = implementation
        self.chat_service = chat_service

    def get_by_id(self, chat_id: int) -> Message | None:
        return self.imp.get_by_id(chat_id)

    def get_user_messages(self, user_id: int) -> list[Message]:
        return self.imp.get_user_messages(user_id)

    def create(self, message_in: MessageIn, owner_id: int) -> Message:
        chat = self.chat_service.get_by_id(message_in.chat_id)

        if not chat:
            raise ChatDoesntExist

        if owner_id not in chat.users_ids:
            raise UserNotInChat

        return self.imp.create(message_in, owner_id)

    def delete_message(self, message_id: int) -> Message | None:
        message = self.imp.delete_message(message_id)

        if message:
            self.chat_service.message_deleted(message)

        return message


class MessageServiceFactory(ABC):
    @abstractmethod
    def create_message_service(self) -> Generator[MessageService, None, None]:
        raise NotImplementedError


class RAMMessageServiceFactory(MessageServiceFactory):
    def __init__(self, crud_factory: Callable[[], RAMMessageCrud], chat_service_factory: ChatServiceFactory) -> None:
        self.crud_factory = crud_factory
        self.chat_service_factory = chat_service_factory

    def create_message_service(self) -> Generator[MessageService, None, None]:
        crud = self.crud_factory()
        imp = RAMMessageServiceImp(crud)
        user_service = self.chat_service_factory.create_chat_service()
        yield MessageService(imp, next(user_service))
