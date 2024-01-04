from ..models.chat import Chat
from ..models.user import UserId


class ChatService:
    def create_chat(self, title: str, users_ids: list[UserId]) -> Chat:
        return Chat(
            id=None,
            title=title,
            users_ids=users_ids,
        )
