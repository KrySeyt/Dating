from typing import Iterable

from .schema import Chat

CHATS_DB: list[Chat] = []


class RAMChatCrud:
    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        chat_id = max(CHATS_DB, key=lambda x: x.id).id if CHATS_DB else 1
        chat = Chat(id=chat_id, users_ids=list(users_ids))
        CHATS_DB.append(chat)
        return chat
