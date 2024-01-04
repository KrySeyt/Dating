from dataclasses import dataclass
from typing import NewType

from .user import UserId
from .chat import ChatId

MessageId = NewType("MessageId", int)


@dataclass(frozen=True)
class Message:
    id: MessageId | None
    text: str
    author_id: UserId
    owner_id: UserId
    chat_id: ChatId
