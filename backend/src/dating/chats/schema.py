from dataclasses import dataclass, field

from ..schema import BaseSchema


@dataclass
class ChatBase(BaseSchema):
    users_ids: list[int]


@dataclass
class Chat(ChatBase):
    id: int
    messages_story: list[int] = field(default_factory=list)


@dataclass
class ChatOut(ChatBase):
    id: int
