from dataclasses import dataclass
from typing import NewType

UserId = NewType("UserId", int)


@dataclass(frozen=True)
class User:
    id: UserId
    username: str
    hashed_password: str
