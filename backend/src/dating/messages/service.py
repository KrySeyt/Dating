from abc import ABC, abstractmethod
from typing import Generator, Callable, Iterable

from .exceptions import MessageNotFound
from .schema import Message, MessageIn, MessageHide
from .crud import RAMMessageCrud
from ..chats.service import ChatService, ChatServiceFactory
from ..chats.exceptions import ChatUnavailableForUser, ChatNotFound
from ..users.exceptions import UserNotFound
from ..users.service import UserService, UserServiceFactory


class MessageServiceImp(ABC):
    @abstractmethod
    def get_by_id(self, message_id: int) -> Message | None:
        raise NotImplementedError

    @abstractmethod
    def get_messages_by_ids(self, messages_ids: Iterable[int]) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    def get_user_messages(self, user_id: int, offset: int, limit: int) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    def get_user_messages_hides_for_chat(self, user_id: int, chat_id: int) -> list[MessageHide]:
        raise NotImplementedError

    @abstractmethod
    def hide_message(self, message_id: int, chat_id: int, user_id: int) -> MessageHide:
        raise NotImplementedError

    @abstractmethod
    def create(self, message_in: MessageIn, owner_id: int) -> Message:
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, message_id: int) -> Message:
        raise NotImplementedError


class RAMMessageServiceImp(MessageServiceImp):
    def __init__(self, crud: RAMMessageCrud) -> None:
        self.db = crud

    def get_by_id(self, message_id: int) -> Message | None:
        return self.db.get_by_id(message_id)

    def get_messages_by_ids(self, messages_ids: Iterable[int]) -> list[Message]:
        return self.db.get_messages_by_ids(messages_ids)

    def get_user_messages(self, user_id: int, offset: int, limit: int) -> list[Message]:
        return self.db.get_user_messages(user_id, offset, limit)

    def get_user_messages_hides_for_chat(self, user_id: int, chat_id: int) -> list[MessageHide]:
        return self.db.get_user_messages_hides_for_chat(user_id, chat_id)

    def hide_message(self, message_id: int, chat_id: int, user_id: int) -> MessageHide:
        return self.db.hide_message(message_id, chat_id, user_id)

    def create(self, message_in: MessageIn, owner_id: int) -> Message:
        return self.db.create(message_in, owner_id)

    def delete_message(self, message_id: int) -> Message:
        return self.db.delete(message_id)


class MessageService:
    def __init__(self, implementation: MessageServiceImp, chat_service: ChatService, user_service: UserService) -> None:
        self.imp = implementation
        self.chat_service = chat_service
        self.user_service = user_service

    def get_by_id(self, message_id: int) -> Message | None:
        return self.imp.get_by_id(message_id)

    def get_user_messages(self, user_id: int, offset: int, limit: int) -> list[Message]:
        user = self.user_service.get_user_by_id(user_id)

        if not user:
            raise UserNotFound

        return self.imp.get_user_messages(user_id, offset, limit)

    def get_messages_by_ids(self, messages_ids: Iterable[int]) -> list[Message]:
        return self.imp.get_messages_by_ids(messages_ids)

    def get_user_messages_hides_for_chat(self, user_id: int, chat_id: int) -> list[MessageHide]:
        return self.imp.get_user_messages_hides_for_chat(user_id, chat_id)

    def create(self, message_in: MessageIn, owner_id: int) -> Message:
        chat = self.chat_service.get_by_id(message_in.chat_id)

        if not chat:
            raise ChatNotFound

        if owner_id not in chat.users_ids:
            raise ChatUnavailableForUser

        message = self.imp.create(message_in, owner_id)
        self.chat_service.add_message_to_chat(chat.id, message.id)

        return message

    def delete_message(self, message_id: int) -> Message:
        message = self.imp.delete_message(message_id)
        self.chat_service.delete_message_from_chat(message.chat_id, message_id)

        for forwarded_chat_id in message.forwarded_chats:
            self.chat_service.message_deleted_from_chat(forwarded_chat_id, message_id)

        return message

    def hide_message(self, message_id: int, chat_id: int, user_id: int) -> MessageHide:
        chat = self.chat_service.get_by_id(chat_id)

        if not chat:
            raise ChatNotFound

        if user_id not in chat.users_ids:
            raise UserNotFound

        if message_id not in chat.messages_story:
            raise MessageNotFound

        hide = self.imp.hide_message(message_id, chat_id, user_id)
        self.chat_service.message_hided_in_chat(chat_id, message_id, user_id)
        return hide


class MessageServiceFactory(ABC):
    @abstractmethod
    def create_message_service(self) -> Generator[MessageService, None, None]:
        raise NotImplementedError


class RAMMessageServiceFactory(MessageServiceFactory):
    def __init__(
            self,
            crud_factory: Callable[[], RAMMessageCrud],
            chat_service_factory: ChatServiceFactory,
            user_service_factory: UserServiceFactory,
    ) -> None:
        self.crud_factory = crud_factory
        self.chat_service_factory = chat_service_factory
        self.user_service_factory = user_service_factory

    def create_message_service(self) -> Generator[MessageService, None, None]:
        crud = self.crud_factory()
        imp = RAMMessageServiceImp(crud)
        chat_service_gen = self.chat_service_factory.create_chat_service()
        user_service_gen = self.user_service_factory.create_user_service()
        yield MessageService(imp, next(chat_service_gen), next(user_service_gen))
