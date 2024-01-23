from typing import Type

from passlib.ifc import PasswordHash

from dating.application.common.password_provider import PasswordProvider


class HashingPasswordProvider(PasswordProvider):
    def __init__(self, hasher: PasswordHash | Type[PasswordHash]) -> None:
        self._hasher = hasher

    def hash_password(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify_password(self, password: str, target_hashed_password: str) -> bool:
        print(password)
        print(target_hashed_password)
        return bool(self._hasher.verify(password, target_hashed_password))
