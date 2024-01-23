from dataclasses import asdict

from dating.adapters.database.exceptions import UserNotFound
from dating.application.common.user_gateway import UserGateway
from dating.domain.models.user import UserId, User


class RAMUserGateway(UserGateway):
    RAM_USERS_DB: list[User] = []
    next_user_id = 0

    def save_user(self, user: User) -> User:
        user_in_db = User(
            **asdict(user) | {"id": self.next_user_id}
        )
        self.next_user_id += 1

        self.RAM_USERS_DB.append(user_in_db)

        return user_in_db

    def get_user_by_id(self, id_: UserId) -> User:
        for user in self.RAM_USERS_DB:
            if user.id == id_:
                return user

        raise UserNotFound(f"User with id {id_} not found")

    def get_user_by_username(self, username: str) -> User:
        for user in self.RAM_USERS_DB:
            if user.username == username:
                return user

        raise UserNotFound(f"User with username {username} not found")

    def delete_user_by_id(self, id_: UserId) -> User:
        user = self.get_user_by_id(id_)
        self.RAM_USERS_DB.remove(user)
        return user
