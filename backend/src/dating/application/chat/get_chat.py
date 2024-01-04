from dating.application.common.chat_gateway import ChatGateway
from dating.application.common.interactor import Interactor
from dating.domain.models.chat import Chat, ChatId


class GetChat(Interactor[ChatId, Chat]):
    def __init__(self, chat_gateway: ChatGateway):
        self._chat_gateway = chat_gateway

    def __call__(self, chat_id: ChatId) -> Chat:
        return self._chat_gateway.get_chat_by_id(chat_id)


