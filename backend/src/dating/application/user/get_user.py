from dataclasses import dataclass

from dating.application.common.interactor import Interactor
from dating.application.common.user_gateway import UserGateway
from dating.domain.models.user import UserId
from dating.domain.services.user import UserService


@dataclass
class UserDTO:
    id: UserId
    username: str


class GetUser(Interactor[UserId, UserDTO]):
    def __init__(self, user_service: UserService, user_gateway: UserGateway) -> None:
        self._user_service = user_service
        self._user_gateway = user_gateway

    def __call__(self, data: UserId) -> UserDTO:
        user = self._user_gateway.get_user_by_id(data)

        assert user.id is not None

        return UserDTO(
            id=user.id,
            username=user.username
        )
