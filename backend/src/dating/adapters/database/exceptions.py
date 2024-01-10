class GatewayException(Exception):
    pass


class ChatNotFound(GatewayException):
    pass


class UserNotFound(GatewayException):
    pass
