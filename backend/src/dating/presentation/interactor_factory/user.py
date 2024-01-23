from abc import ABC, abstractmethod
from typing import ContextManager

from dating.application.user.create_user import CreateUser
from dating.application.user.get_user import GetUser
from dating.application.user.login import Login


class UserInteractorFactory(ABC):
    @abstractmethod
    def get_user(self) -> ContextManager[GetUser]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self) -> ContextManager[CreateUser]:
        raise NotImplementedError

    @abstractmethod
    def login(self) -> ContextManager[Login]:
        raise NotImplementedError
