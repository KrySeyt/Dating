from dataclasses import dataclass, field

from dating.schema import BaseSchema


@dataclass
class MessageBase(BaseSchema):
    chat_id: int
    text: str


@dataclass
class Message(MessageBase):
    id: int
    owner_id: int
    forwarded_chats: list[int] = field(default_factory=list)


@dataclass
class MessageIn(MessageBase):
    pass


@dataclass
class MessageOut(MessageBase):
    id: int
    owner_id: int


@dataclass
class MessageHideBase:
    message_id: int
    chat_id: int
    user_id: int


@dataclass
class MessageHide(MessageHideBase):
    pass


@dataclass
class MessageHideOut(MessageHideBase):
    pass
