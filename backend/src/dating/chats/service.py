from abc import ABC, abstractmethod
from typing import Generator, Callable, Iterable

# from sqlalchemy import Engine
# from sqlalchemy.orm import Session

from .schema import Chat
from .crud import RAMChatCrud
from ..users.service import UserService, UserServiceFactory
from ..users.exceptions import UserNotFound
from ..messages.schema import Message


class ChatServiceImp(ABC):
    @abstractmethod
    def get_by_id(self, chat_id: int) -> Chat | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_chats(self, user_id: int) -> list[Chat]:
        raise NotImplementedError

    @abstractmethod
    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def delete_chat(self, chat_id: int) -> Chat | None:
        raise NotImplementedError

    @abstractmethod
    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat | None:
        raise NotImplementedError


class RAMChatServiceImp(ChatServiceImp):
    def __init__(self, crud: RAMChatCrud) -> None:
        self.db = crud

    def get_by_id(self, chat_id: int) -> Chat | None:
        return self.db.get_by_id(chat_id)

    def get_user_chats(self, user_id: int) -> list[Chat]:
        return self.db.get_user_chats(user_id)

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        return self.db.create_chat(users_ids)

    def delete_chat(self, chat_id: int) -> Chat | None:
        return self.db.delete_chat(chat_id)

    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat | None:
        return self.db.delete_chat_for_user(chat_id, user_id)


# class RDBMSChatServiceImp(ChatServiceImp):
#     def __init__(self, crud: ChatCrud) -> None:
#         self.crud = crud
#


class ChatService:
    def __init__(self, implementation: ChatServiceImp, user_service: UserService) -> None:
        self.imp = implementation
        self.user_service = user_service

    def get_by_id(self, chat_id: int) -> Chat | None:
        return self.imp.get_by_id(chat_id)

    def get_user_chats(self, user_id: int) -> list[Chat]:
        return self.imp.get_user_chats(user_id)

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        for user_id in users_ids:
            if not self.user_service.get_user_by_id(user_id):
                raise UserNotFound(f"User with id {user_id} doesn't exists")

        return self.imp.create_chat(users_ids)

    def create_chat_with_matched_user(self, user_id: int) -> Chat | None:
        user_chats = self.get_user_chats(user_id)
        except_users: set[int] = set()
        for chat in user_chats:
            for id_ in chat.users_ids:
                except_users.add(id_)

        second_user = self.user_service.get_random_user(except_=except_users)

        if not second_user:
            return None

        return self.create_chat((user_id, second_user.id))

    def new_message(self, message: Message) -> None:
        pass

    def delete_chat(self, chat_id: int) -> Chat | None:
        return self.imp.delete_chat(chat_id)

    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat | None:
        return self.imp.delete_chat_for_user(chat_id, user_id)


class ChatServiceFactory(ABC):
    @abstractmethod
    def create_chat_service(self) -> Generator[ChatService, None, None]:
        raise NotImplementedError


class RAMChatServiceFactory(ChatServiceFactory):
    def __init__(self, crud_factory: Callable[[], RAMChatCrud], user_service_factory: UserServiceFactory) -> None:
        self.crud_factory = crud_factory
        self.user_service_factory = user_service_factory

    def create_chat_service(self) -> Generator[ChatService, None, None]:
        crud = self.crud_factory()
        imp = RAMChatServiceImp(crud)
        user_service = self.user_service_factory.create_user_service()
        yield ChatService(imp, next(user_service))


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
