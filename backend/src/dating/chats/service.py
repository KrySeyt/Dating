from abc import ABC, abstractmethod
from typing import Generator, Callable, Iterable

# from sqlalchemy import Engine
# from sqlalchemy.orm import Session

from .schema import Chat
from .crud import RAMChatCrud


class ChatServiceImp(ABC):
    @abstractmethod
    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        raise NotImplementedError


class RAMChatServiceImp(ChatServiceImp):
    def __init__(self, crud: RAMChatCrud) -> None:
        self.db = crud

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        return self.db.create_chat(users_ids)


# class RDBMSChatServiceImp(ChatServiceImp):
#     def __init__(self, crud: ChatCrud) -> None:
#         self.crud = crud
#


class ChatService:
    def __init__(self, implementation: ChatServiceImp) -> None:
        self.imp = implementation

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        return self.imp.create_chat(users_ids)


class ChatServiceFactory(ABC):
    @abstractmethod
    def create_chat_service(self) -> Generator[ChatService, None, None]:
        raise NotImplementedError


class RAMChatServiceFactory(ChatServiceFactory):
    def __init__(self, crud_factory: Callable[[], RAMChatCrud]) -> None:
        self.crud_factory = crud_factory

    def create_chat_service(self) -> Generator[ChatService, None, None]:
        crud = self.crud_factory()
        imp = RAMChatServiceImp(crud)
        yield ChatService(imp)


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
