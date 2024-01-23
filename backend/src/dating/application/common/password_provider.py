from abc import abstractmethod, ABC


class PasswordProvider(ABC):  # TODO: mb better naming?
    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, password: str, target_hashed_password: str) -> bool:
        raise NotImplementedError
