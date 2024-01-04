from dataclasses import dataclass
from typing import NewType

from .user import UserId

NotificationsSettingsId = NewType("NotificationsSettingsId", int)


@dataclass(frozen=True)
class NotificationsSettings:
    user_id: UserId
    websocket_uri: str
