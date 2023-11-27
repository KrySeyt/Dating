from dataclasses import dataclass


@dataclass
class MessageBase:
    chat_id: int
    text: str


@dataclass
class Message(MessageBase):
    id: int
    owner_id: int


@dataclass
class MessageIn(MessageBase):
    pass


@dataclass
class MessageOut(MessageBase):
    id: int
    owner_id: int
