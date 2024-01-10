from abc import ABC, abstractmethod
from typing import ContextManager

from dating.application.user.create_user import CreateUser
from dating.application.user.get_user import GetUser


class UserInteractorFactory(ABC):
    @abstractmethod
    def get_user(self) -> ContextManager[GetUser]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self) -> ContextManager[CreateUser]:
        raise NotImplementedError

    # @abstractmethod
    # def delete_user(self) -> ContextManager[DeleteChat]:
    #     raise NotImplementedError
