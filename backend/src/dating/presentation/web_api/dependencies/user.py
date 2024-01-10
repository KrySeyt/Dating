from typing import Annotated

from fastapi import Body


def get_hashed_password(password: Annotated[str, Body(embed=True)]) -> str:
    return str(hash(password))  # Just mock
