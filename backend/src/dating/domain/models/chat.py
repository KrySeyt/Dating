from dataclasses import dataclass
from typing import NewType

from .user import UserId

ChatId = NewType("ChatId", int)


@dataclass
class Chat:
    id: ChatId
    title: str
    users_ids: list[UserId]
