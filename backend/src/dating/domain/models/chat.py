from dataclasses import dataclass
from typing import NewType

from .user import UserId

ChatId = NewType("ChatId", int)


@dataclass(frozen=True)
class Chat:
    id: ChatId | None
    title: str
    users_ids: list[UserId]
