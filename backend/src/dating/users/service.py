from abc import ABC, abstractmethod
from typing import Generator, Callable, Container

# from sqlalchemy import Engine
# from sqlalchemy.orm import Session

from .schema import UserIn, User
from .crud import RAMUserCrud
from .exceptions import UserAlreadyExists


class UserServiceImp(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_random_user(self, except_: Container[int]) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def register(self, user: UserIn) -> User:
        raise NotImplementedError


class RAMUserServiceImp(UserServiceImp):
    def __init__(self, crud: RAMUserCrud) -> None:
        self.db = crud

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.get_user_by_username(username)

    def get_random_user(self, except_: Container[int]) -> User | None:
        return self.db.get_random_user(except_)

    def register(self, user: UserIn) -> User:
        return self.db.create_user(user)


# class RDBMSUserServiceImp(UserServiceImp):
#     def __init__(self, crud: UserCrud) -> None:
#         self.crud = crud
#
#     def get_user_by_id(self, user_id: int) -> User | None:
#         user_model = self.crud.get_user_by_id(user_id)
#
#         if not user_model:
#             return None
#
#         return User.from_object(user_model)
#
#     def get_user_by_username(self, username: str) -> User | None:
#         user_model = self.crud.get_user_by_username(username)
#
#         if not user_model:
#             return None
#
#         return User.from_object(user_model)
#
#     def register(self, user: UserIn) -> User:
#         user_model = self.crud.create_user(user)
#         return User.from_object(user_model)


class UserService:
    def __init__(self, implementation: UserServiceImp) -> None:
        self.imp = implementation

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.imp.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.imp.get_user_by_username(username)

    def get_random_user(self, except_: Container[int]) -> User | None:
        return self.imp.get_random_user(except_)

    def register(self, user: UserIn) -> User:
        if not self.get_user_by_username(user.username):
            return self.imp.register(user)
        raise UserAlreadyExists("Username already occupied")


class UserServiceFactory(ABC):
    @abstractmethod
    def create_user_service(self) -> Generator[UserService, None, None]:
        raise NotImplementedError


class RAMUserServiceFactory(UserServiceFactory):
    def __init__(self, crud_factory: Callable[[], RAMUserCrud]) -> None:
        self.crud_factory = crud_factory

    def create_user_service(self) -> Generator[UserService, None, None]:
        crud = self.crud_factory()
        imp = RAMUserServiceImp(crud)
        yield UserService(imp)


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
