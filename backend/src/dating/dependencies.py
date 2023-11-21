from typing import Callable, Any, NoReturn


class Stub:
    def __init__(self, dependency: Callable[..., Any]) -> None:
        self._dependency = dependency

    def __call__(self) -> NoReturn:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        return bool(self._dependency == other)

    def __hash__(self) -> int:
        return hash(self._dependency)


Dataclass = dict[str, Any]

