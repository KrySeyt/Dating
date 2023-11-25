from uuid import uuid4

from .crud import SessionCrud


SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 7


class AuthenticationError(ValueError):
    pass


class SessionProvider:
    def __init__(self, crud: SessionCrud) -> None:
        self.crud = crud

    def create_token(self, user_id: int) -> str:
        token = str(uuid4())
        self.crud.add_session(token, user_id)
        return token

    def validate_token(self, token: str) -> int:
        if not self.crud.session_exists(token):
            raise AuthenticationError
        return self.crud.get_user_id(token)

    def expire_token(self, token: str) -> None:
        self.crud.delete_session(token)
