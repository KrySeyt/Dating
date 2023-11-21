from dataclasses import dataclass, fields
from typing import Any, Self


@dataclass
class BaseSchema:
    @classmethod
    def from_object(cls, obj: object) -> Self:
        self_dict: dict[str, Any] = {}
        for field in fields(cls):
            self_dict[field.name] = getattr(obj, field.name)

        return cls(**self_dict)
