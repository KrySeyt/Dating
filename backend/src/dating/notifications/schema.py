from dataclasses import dataclass

from dating.messages.schema import MessageOut


@dataclass
class NewMessageOut:
    chat_id: int
    message: MessageOut
