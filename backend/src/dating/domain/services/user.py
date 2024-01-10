from ..models.user import User


class UserService:
    def create_user(self, username: str, hashed_password: str) -> User:
        return User(
            id=None,
            username=username,
            hashed_password=hashed_password,
        )

    def update_user(self, user: User, new_username: str, new_hashed_password: str) -> User:
        return User(
            id=user.id,
            username=new_username,
            hashed_password=new_hashed_password,
        )
