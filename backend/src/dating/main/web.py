from typing import TypeVar, Callable

from fastapi import FastAPI

from dating.main.ioc import ChatIoC
from dating.presentation.interactor_factory.chat import ChatInteractorFactory

DependencyT = TypeVar("DependencyT")


def singleton(dependency: DependencyT) -> Callable[[], DependencyT]:
    return lambda: dependency


def create_app() -> FastAPI:
    app = FastAPI()
    chat_ioc = ChatIoC()

    app.dependency_overrides[ChatInteractorFactory] = singleton(chat_ioc)

    return app
