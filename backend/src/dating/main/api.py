from fastapi import FastAPI, APIRouter
from passlib.ifc import PasswordHash
from passlib.hash import argon2

from ..users.router import users_router
from ..chats.router import chats_router
from ..messages.router import messages_router
from ..users.service import RAMUserServiceFactory, UserService
from ..chats.service import RAMChatServiceFactory, ChatService
from ..messages.service import RAMMessageServiceFactory, MessageService
from ..users.crud import RAMUserCrud, RAMSessionCrud
from ..chats.crud import RAMChatCrud
from ..messages.crud import RAMMessageCrud
from ..users.security import SessionProvider


def create_app() -> FastAPI:
    app_router = APIRouter(prefix="/api/v1")
    app_router.include_router(users_router)
    app_router.include_router(chats_router)
    app_router.include_router(messages_router)

    app = FastAPI(version="1")
    app.include_router(app_router)

    user_service_factory = RAMUserServiceFactory(RAMUserCrud)
    app.dependency_overrides[UserService] = user_service_factory.create_user_service

    chat_service_factory = RAMChatServiceFactory(RAMChatCrud, user_service_factory)
    app.dependency_overrides[ChatService] = chat_service_factory.create_chat_service

    message_service_factory = RAMMessageServiceFactory(RAMMessageCrud, chat_service_factory, user_service_factory)
    app.dependency_overrides[MessageService] = message_service_factory.create_message_service

    ram_session_crud = RAMSessionCrud()
    session_provider = SessionProvider(ram_session_crud)
    app.dependency_overrides[SessionProvider] = lambda: session_provider

    hasher = argon2
    app.dependency_overrides[PasswordHash] = lambda: hasher

    return app


app = create_app()
