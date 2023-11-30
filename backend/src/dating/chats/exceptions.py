from ..users.exceptions import UserHasNoPermission


class UserNotInChat(ValueError):
    pass


class ChatNotFound(ValueError):
    pass


class ChatUnavailableForUser(UserHasNoPermission):
    pass
