import uuid
from dataclasses import dataclass

from dating.application.common.interactor import Interactor
from dating.application.common.password_provider import PasswordProvider
from dating.application.common.session_gateway import SessionGateway, SessionToken
from dating.application.common.user_gateway import UserGateway
from dating.domain.services.user import UserService


class WrongCredentials(Exception):
    pass


@dataclass
class LoginDTO:
    username: str
    password: str


class Login(Interactor[LoginDTO, SessionToken]):
    def __init__(
            self,
            user_service: UserService,
            user_gateway: UserGateway,
            session_gateway: SessionGateway,
            password_provider: PasswordProvider,
    ) -> None:
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._session_gateway = session_gateway
        self._password_provider = password_provider

    def __call__(self, data: LoginDTO) -> SessionToken:
        user = self._user_gateway.get_user_by_username(data.username)
        assert user.id is not None

        if not self._password_provider.verify_password(data.password, user.hashed_password):
            raise WrongCredentials

        token = uuid.uuid4()

        self._session_gateway.save_session_token(user.id, SessionToken(str(token)))

        return SessionToken(str(token))
