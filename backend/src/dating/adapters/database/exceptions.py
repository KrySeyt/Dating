class GatewayException(Exception):
    pass


class ChatNotFound(GatewayException):
    pass


class UserNotFound(GatewayException):
    pass


class SessionNotFound(GatewayException):
    pass
