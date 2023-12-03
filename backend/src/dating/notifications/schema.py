from dataclasses import dataclass
from enum import Enum

from dating.messages.schema import MessageOut


class MessageEventsType(str, Enum):
    NEW = "new_message"
    DELETED = "message_deleted"


@dataclass
class MessageEventOut:
    type: MessageEventsType
    message: MessageOut
