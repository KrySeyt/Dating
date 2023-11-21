from dataclasses import dataclass

from ..schema import BaseSchema


@dataclass
class UserBase(BaseSchema):
    username: str


@dataclass
class User(UserBase):
    id: int
    hashed_password: str


@dataclass
class RawUserIn(UserBase):
    password: str

    def __post_init__(self) -> None:
        if not self.password:
            raise ValueError("No password")


@dataclass
class UserIn(UserBase):
    hashed_password: str

    def __post_init__(self) -> None:
        if not self.hashed_password:
            raise ValueError("No password")


@dataclass
class UserOut(UserBase):
    id: int


@dataclass
class LoginData:
    username: str
    password: str
