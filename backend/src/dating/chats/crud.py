from typing import Iterable

from .exceptions import ChatNotFound, ChatUnavailableForUser
from .schema import Chat
from ..messages.exceptions import MessageNotFound

CHATS_DB: list[Chat] = []


class RAMChatCrud:
    def get_by_id(self, chat_id: int) -> Chat | None:
        for chat in CHATS_DB:
            if chat.id == chat_id:
                return chat

        return None

    def get_user_chats(self, user_id: int, offset: int, limit: int) -> list[Chat]:
        chats: list[Chat] = []
        for chat in CHATS_DB:
            if user_id in chat.users_ids:
                chats.append(chat)
        return chats[offset:limit + offset]

    def get_all_user_chats(self, user_id: int) -> list[Chat]:
        chats: list[Chat] = []
        for chat in CHATS_DB:
            if user_id in chat.users_ids:
                chats.append(chat)
        return chats

    def get_chat_messages_ids(self, chat_id: int, offset: int, limit: int) -> list[int]:
        chat = self.get_by_id(chat_id)

        if not chat:
            raise ChatNotFound

        return chat.messages_story[offset:limit + offset]

    def create_chat(self, users_ids: Iterable[int]) -> Chat:
        chat_id = max(CHATS_DB, key=lambda x: x.id).id + 1 if CHATS_DB else 1
        chat = Chat(id=chat_id, users_ids=list(users_ids))
        CHATS_DB.append(chat)
        return chat

    def add_message_to_chat(self, chat_id: int, message_id: int) -> Chat:
        chat = self.get_by_id(chat_id)

        if not chat:
            raise ChatNotFound

        chat.messages_story.insert(0, message_id)
        return chat

    def delete_message_from_chat(self, chat_id: int, message_id: int) -> Chat:
        chat = self.get_by_id(chat_id)

        if not chat:
            raise ChatNotFound

        if message_id not in chat.messages_story:
            raise MessageNotFound

        chat.messages_story.remove(message_id)
        return chat

    def delete_chat(self, chat_id: int) -> Chat:
        chat = self.get_by_id(chat_id)

        if not chat:
            raise ChatNotFound

        CHATS_DB.remove(chat)
        return chat

    def delete_chat_for_user(self, chat_id: int, user_id: int) -> Chat:
        chat = self.get_by_id(chat_id)

        if not chat:
            raise ChatNotFound

        if user_id not in chat.users_ids:
            raise ChatUnavailableForUser

        chat.users_ids.remove(user_id)
        return chat
