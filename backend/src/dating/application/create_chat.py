from dataclasses import dataclass

from .common.chat_gateway import ChatGateway
from .common.interactor import Interactor
from ..domain.models.chat import Chat
from ..domain.models.user import UserId
from ..domain.services.chat import ChatService


@dataclass
class NewChatDTO:
    title: str
    user_ids: list[UserId]


class CreateChat(Interactor[NewChatDTO, Chat]):
    def __init__(self, chat_service: ChatService, chat_gateway: ChatGateway):
        self._chat_service = chat_service
        self._chat_gateway = chat_gateway

    def __call__(self, data: NewChatDTO) -> Chat:
        chat = self._chat_service.create_chat(
            title=data.title,
            users_ids=NewChatDTO.user_ids,
        )

        chat = self._chat_gateway.save_chat(chat)

        return chat
