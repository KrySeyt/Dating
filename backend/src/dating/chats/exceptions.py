from ..users.exceptions import UserHasNoPermission


class ChatNotFound(ValueError):
    pass


class ChatUnavailableForUser(UserHasNoPermission):
    pass
