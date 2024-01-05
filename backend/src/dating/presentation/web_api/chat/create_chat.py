from typing import Annotated

from fastapi import Depends

from dating.application.chat.create_chat import NewChatDTO
from dating.domain.models.chat import Chat
from .router import chat_router
from ...interactor_factory.chat import ChatInteractorFactory


@chat_router.post("/")
def create_chat(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        data: NewChatDTO,
) -> Chat:
    with interactor_factory.create_chat() as create_chat_interactor:
        return create_chat_interactor(data)
