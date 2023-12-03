import logging
import json
from dataclasses import asdict
from abc import ABC, abstractmethod
from typing import Generator

from websockets.sync import client

from dating.messages.crud import RAMMessageCrud
from dating.messages.schema import MessageOut, Message
from dating.notifications.schema import MessageEventOut, MessageEventsType
from dating.users.service import UserService, UserServiceFactory


logger = logging.getLogger(__name__)


class NotificationServiceImp(ABC):
    @abstractmethod
    def notify_new_message(self, user_id: int, message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def notify_message_deleted(self, user_id: int, message: Message) -> None:
        raise NotImplementedError


class WebsocketNotificationServiceImp(NotificationServiceImp):
    def __init__(self, user_service: UserService, message_crud: RAMMessageCrud) -> None:  # Shit code bcs of shit design
        self.user_service = user_service
        self.message_crud = message_crud

    def notify_new_message(self, user_id: int, message: Message) -> None:
        user_websocket_uri = self.user_service.get_user_websocket_uri(user_id)

        if not user_websocket_uri:
            return

        try:
            with client.connect(user_websocket_uri) as websocket:
                message_event = MessageEventOut(type=MessageEventsType.NEW, message=MessageOut.from_object(message))
                websocket.send(json.dumps(asdict(message_event)))
        except OSError as err:
            logger.error(err)

    def notify_message_deleted(self, user_id: int, message: Message) -> None:
        user_websocket_uri = self.user_service.get_user_websocket_uri(user_id)

        if not user_websocket_uri:
            return

        try:
            with client.connect(user_websocket_uri) as websocket:
                message_event = MessageEventOut(type=MessageEventsType.DELETED, message=MessageOut.from_object(message))
                websocket.send(json.dumps(asdict(message_event)))
        except OSError as err:
            logger.error(err)


class NotificationService:
    def __init__(self, implementation: NotificationServiceImp) -> None:
        self.imp = implementation

    def notify_new_message(self, user_id: int, message: Message) -> None:
        self.imp.notify_new_message(user_id, message)

    def notify_message_deleted(self, user_id: int, message: Message) -> None:
        self.imp.notify_message_deleted(user_id, message)


class NotificationServiceFactory(ABC):
    @abstractmethod
    def create_notification_service(self) -> Generator[NotificationService, None, None]:
        raise NotImplementedError


class RAMNotificationServiceFactory(NotificationServiceFactory):
    def __init__(
            self,
            user_service_factory: UserServiceFactory,
    ) -> None:

        self.user_service_factory = user_service_factory

    def create_notification_service(self) -> Generator[NotificationService, None, None]:
        user_service_gen = self.user_service_factory.create_user_service()
        imp = WebsocketNotificationServiceImp(next(user_service_gen), RAMMessageCrud())
        yield NotificationService(imp)
