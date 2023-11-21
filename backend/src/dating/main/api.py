from fastapi import FastAPI
from passlib.ifc import PasswordHash
from passlib.hash import argon2

from ..users.router import users_router
from ..users.service import RAMUserServiceFactory, UserService
from ..users.crud import RAMUserCrud, RAMSessionCrud
from ..users.security import SessionProvider


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users_router)

    user_service_factory = RAMUserServiceFactory(RAMUserCrud)
    app.dependency_overrides[UserService] = user_service_factory.create_user_service

    ram_session_crud = RAMSessionCrud()
    session_provider = SessionProvider(ram_session_crud)
    app.dependency_overrides[SessionProvider] = lambda: session_provider

    hasher = argon2
    app.dependency_overrides[PasswordHash] = lambda: hasher

    return app


app = create_app()
