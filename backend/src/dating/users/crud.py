from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Container

# from sqlalchemy import select
# from sqlalchemy.orm import Session
# from redis import Redis

# from . import models
from . import schema
from .exceptions import UserNotFound

# class PostgresUserCrud:
#     def __init__(self, session: Session) -> None:
#         self.db = session
#
#     def get_user_by_id(self, user_id: int) -> models.User | None:
#         return self.db.get(models.User, user_id)
#
#     def get_user_by_username(self, username: str) -> models.User | None:
#         return self.db.scalar(select(models.User).where(models.User.username == username))
#
#     def create_user(self, user: schema.UserIn) -> models.User:
#         user_model = models.User(**asdict(user))
#
#         self.db.add(user_model)
#
#         self.db.commit()
#         self.db.refresh(user_model)
#
#         return user_model

USERS_DB: list[schema.User] = []


class RAMUserCrud:
    def get_user_by_id(self, user_id: int) -> schema.User | None:
        for user in USERS_DB:
            if user.id == user_id:
                return user
        return None

    def get_user_by_username(self, username: str) -> schema.User | None:
        for user in USERS_DB:
            if user.username == username:
                return user
        return None

    def get_random_user(self, except_: Container[int]) -> schema.User | None:
        for user in USERS_DB:
            if user.id not in except_:
                return user

        return None

    def create_user(self, user_in: schema.UserIn) -> schema.User:
        user_id = max(user.id for user in USERS_DB) + 1 if USERS_DB else 1
        user = schema.User(id=user_id, **asdict(user_in))
        USERS_DB.append(user)
        return user

    def update_user(self, user_id: int, user_in: schema.UserIn) -> schema.User:
        user = self.get_user_by_id(user_id)

        if not user:
            raise UserNotFound

        user.username = user_in.username
        user.hashed_password = user_in.hashed_password
        return user


class SessionCrud(ABC):
    @abstractmethod
    def get_user_id(self, token: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def session_exists(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_session(self, token: str, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_session(self, token: str) -> None:
        raise NotImplementedError


Token = str
UserID = int

SESSIONS_DB: dict[Token, UserID] = {}


class RAMSessionCrud(SessionCrud):
    def session_exists(self, token: Token) -> bool:
        return token in SESSIONS_DB

    def get_user_id(self, token: Token) -> UserID:
        return SESSIONS_DB[token]

    def add_session(self, token: Token, user_id: UserID) -> None:
        SESSIONS_DB[token] = user_id

    def delete_session(self, token: Token) -> None:
        del SESSIONS_DB[token]


# class RedisSessionCrud(SessionCrud):
#     def __init__(self, redis: Redis) -> None:
#         self.redis = redis
#
#     def session_exists(self, token: str) -> bool:
#         return self.redis.exists(token)  # type: ignore
#
#     def get_user_id(self, token: str) -> int:
#         return self.redis[token]  # type: ignore
#
#     def add_session(self, token: str, user_id: int) -> None:
#         self.redis[token] = user_id
#
#     def delete_session(self, token: str) -> None:
#         self.redis.delete(token)
