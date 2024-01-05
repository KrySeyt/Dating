from typing import Annotated

from fastapi import Depends, Path

from dating.domain.models.chat import ChatId, Chat
from dating.presentation.web_api.chat.router import chat_router
from dating.presentation.interactor_factory.chat import ChatInteractorFactory


@chat_router.get("/{chat_id}")
def get_chat(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        chat_id: Annotated[int, Path()],
) -> Chat:
    with interactor_factory.get_chat() as get_chat_interactor:
        return get_chat_interactor(ChatId(chat_id))
