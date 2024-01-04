from ..models.user import UserId
from ..models.notification import NotificationsSettings


class NotificationsSettingsService:
    def create_settings(self, user_id: UserId, websocket_uri: str) -> NotificationsSettings:
        return NotificationsSettings(
            user_id=user_id,
            websocket_uri=websocket_uri,
        )

    def update_settings(self, settings: NotificationsSettings, new_websocket_uri: str) -> NotificationsSettings:
        return NotificationsSettings(
            user_id=settings.user_id,
            websocket_uri=new_websocket_uri,
        )
