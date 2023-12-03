from abc import ABC, abstractmethod
from typing import Generator, Callable, Iterable, Container

from .exceptions import ChatNotFound
from .schema import Chat
from .crud import RAMChatCrud
from ..notifications.service import NotificationService, NotificationServiceFactory
from ..users.service import UserService, UserServiceFactory
from ..users.exceptions import UserNotFound


class ChatServiceImp(ABC):
    @abstractmethod
    def get_by_id(self, chat_id: int) -> Chat | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_chats(self, user_id: int, offset: int, limit: int) -> list[Chat]:
        raise NotImplementedError

    @abstractmethod
    def get_all_user_chats(self, user_id: int) -> list[Chat]:
        raise NotImplementedError

    @abstractmethod
    def get_chat_messages_ids(self, chat_id: int, offset: int, limit: int, except_: Container[int]) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def add_message_to_chat(self, chat_id: int, message_id: int) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def delete_message_from_chat(self, chat_id: int, message_id: int) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def delete_chat(self, chat_id: int) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat:
        raise NotImplementedError


class RAMChatServiceImp(ChatServiceImp):
    def __init__(self, crud: RAMChatCrud) -> None:
        self.db = crud

    def get_by_id(self, chat_id: int) -> Chat | None:
        return self.db.get_by_id(chat_id)

    def get_user_chats(self, user_id: int, offset: int, limit: int) -> list[Chat]:
        return self.db.get_user_chats(user_id, offset, limit)

    def get_all_user_chats(self, user_id: int) -> list[Chat]:
        return self.db.get_all_user_chats(user_id)

    def get_chat_messages_ids(self, chat_id: int, offset: int, limit: int, except_: Container[int]) -> list[int]:
        return self.db.get_chat_messages_ids(chat_id, offset, limit, except_)

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        return self.db.create_chat(users_ids)

    def add_message_to_chat(self, chat_id: int, message_id: int) -> Chat:
        return self.db.add_message_to_chat(chat_id, message_id)

    def delete_message_from_chat(self, chat_id: int, message_id: int) -> Chat:
        return self.db.delete_message_from_chat(chat_id, message_id)

    def delete_chat(self, chat_id: int) -> Chat:
        return self.db.delete_chat(chat_id)

    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat:
        return self.db.delete_chat_for_user(chat_id, user_id)


# class RDBMSChatServiceImp(ChatServiceImp):
#     def __init__(self, crud: ChatCrud) -> None:
#         self.crud = crud
#


class ChatService:
    def __init__(
            self,
            implementation: ChatServiceImp,
            user_service: UserService,
            notification_service: NotificationService,
    ) -> None:

        self.imp = implementation
        self.user_service = user_service
        self.notification_service = notification_service

    def get_by_id(self, chat_id: int) -> Chat | None:
        return self.imp.get_by_id(chat_id)

    def get_user_chats(self, user_id: int, offset: int, limit: int) -> list[Chat]:
        user = self.user_service.get_user_by_id(user_id)

        if not user:
            raise UserNotFound

        return self.imp.get_user_chats(user_id, offset, limit)

    def get_all_user_chats(self, user_id: int) -> list[Chat]:
        user = self.user_service.get_user_by_id(user_id)

        if not user:
            raise UserNotFound

        return self.imp.get_all_user_chats(user_id)

    def get_chat_messages_ids(
            self,
            chat_id: int,
            offset: int,
            limit: int,
            except_: Container[int] | None = None
    ) -> list[int]:

        except_chat_ids = except_ or {}
        return self.imp.get_chat_messages_ids(chat_id, offset, limit, except_chat_ids)

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        for user_id in users_ids:
            if not self.user_service.get_user_by_id(user_id):
                raise UserNotFound(f"User with id {user_id} doesn't exists")

        return self.imp.create_chat(users_ids)

    def create_chat_with_matched_user(self, request_user_id: int) -> Chat | None:
        user_chats = self.get_all_user_chats(request_user_id)
        except_users_ids: set[int] = {request_user_id}
        for chat in user_chats:
            for id_ in chat.users_ids:
                except_users_ids.add(id_)

        second_user = self.user_service.get_random_user(except_=except_users_ids)

        if not second_user:
            return None

        return self.create_chat((request_user_id, second_user.id))

    def add_message_to_chat(self, chat_id: int, message_id: int) -> Chat:
        chat = self.imp.add_message_to_chat(chat_id, message_id)
        self.new_message_in_chat(chat_id, message_id)
        return chat

    def delete_message_from_chat(self, chat_id: int, message_id: int) -> Chat:
        chat = self.imp.delete_message_from_chat(chat_id, message_id)
        self.message_deleted_from_chat(chat_id, message_id)
        return chat

    def new_message_in_chat(self, chat_id: int, message_id: int) -> None:
        chat = self.get_by_id(chat_id)

        if chat is None:
            raise ChatNotFound

        users_ids = chat.users_ids

        for user_id in users_ids:
            self.notification_service.notify_new_message(user_id, message_id)

    def message_deleted_from_chat(self, chat_id: int, message_id: int) -> None:
        pass

    def message_hided_in_chat(self, chat_id: int, message_id: int, user_id: int) -> None:
        pass

    def delete_chat(self, chat_id: int) -> Chat:
        return self.imp.delete_chat(chat_id)

    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat:
        return self.imp.delete_chat_for_user(chat_id, user_id)


class ChatServiceFactory(ABC):
    @abstractmethod
    def create_chat_service(self) -> Generator[ChatService, None, None]:
        raise NotImplementedError


class RAMChatServiceFactory(ChatServiceFactory):
    def __init__(
            self,
            crud_factory: Callable[[], RAMChatCrud],
            user_service_factory: UserServiceFactory,
            notification_service_factory: NotificationServiceFactory,
    ) -> None:

        self.crud_factory = crud_factory
        self.user_service_factory = user_service_factory
        self.notification_service_factory = notification_service_factory

    def create_chat_service(self) -> Generator[ChatService, None, None]:
        crud = self.crud_factory()
        imp = RAMChatServiceImp(crud)
        user_service_gen = self.user_service_factory.create_user_service()
        notification_service_gen = self.notification_service_factory.create_notification_service()
        yield ChatService(imp, next(user_service_gen), next(notification_service_gen))


# class RDBMSUserServiceFactory(UserServiceFactory):
#     def __init__(self, engine: Engine, crud_factory: Callable[[Session], UserCrud]) -> None:
#         self.engine = engine
#         self.crud_factory = crud_factory
#
#     def create_user_service(self) -> Generator[UserService, None, None]:
#         with Session(self.engine) as session:
#             crud = self.crud_factory(session)
#             imp = RDBMSUserServiceImp(crud)
#             yield UserService(imp)
