from dataclasses import dataclass

from ..schema import BaseSchema


@dataclass
class ChatBase(BaseSchema):
    users_ids: list[int]


@dataclass
class Chat(ChatBase):
    id: int


@dataclass
class ChatOut(ChatBase):
    id: int
