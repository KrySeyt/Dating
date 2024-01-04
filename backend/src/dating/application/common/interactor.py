from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Interactor(ABC, Generic[InputDTO, OutputDTO]):
    @abstractmethod
    def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError
