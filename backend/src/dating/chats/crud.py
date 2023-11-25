from typing import Iterable

from .schema import Chat


CHATS_DB: list[Chat] = []


class RAMChatCrud:
    def get_by_id(self, chat_id: int) -> Chat | None:
        for chat in CHATS_DB:
            if chat.id == chat_id:
                return chat

        return None

    def get_user_chats(self, user_id: int) -> list[Chat]:
        chats: list[Chat] = []
        for chat in CHATS_DB:
            if user_id in chat.users_ids:
                chats.append(chat)
        return chats

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        chat_id = max(CHATS_DB, key=lambda x: x.id).id + 1 if CHATS_DB else 1
        chat = Chat(id=chat_id, users_ids=list(users_ids))
        CHATS_DB.append(chat)
        return chat

    def delete_chat(self, chat_id: int) -> Chat | None:
        chat = self.get_by_id(chat_id)

        if not chat:
            return None

        CHATS_DB.remove(chat)
        return chat

    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat | None:
        chat = self.get_by_id(chat_id)

        if not chat:
            return None

        if user_id not in chat.users_ids:
            return None

        chat.users_ids.remove(user_id)
        return chat
