from typing import Annotated

from fastapi import Depends, Path, status
from fastapi.exceptions import HTTPException

from dating.adapters.database.exceptions import ChatNotFound
from dating.domain.models.chat import ChatId, Chat
from dating.presentation.web_api.chat.router import chat_router
from dating.presentation.interactor_factory.chat import ChatInteractorFactory


@chat_router.get("/{chat_id}")
def get_chat(
        interactor_factory: Annotated[ChatInteractorFactory, Depends()],
        chat_id: Annotated[int, Path()],
) -> Chat:
    with interactor_factory.get_chat() as get_chat_interactor:
        try:
            return get_chat_interactor(ChatId(chat_id))
        except ChatNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
