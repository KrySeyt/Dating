from typing import Annotated

from fastapi import Body, Depends

from dating.application.common.password_provider import PasswordProvider


def get_hashed_password(
        password: Annotated[str, Body(embed=True)],
        password_provider: Annotated[PasswordProvider, Depends()]
) -> str:
    return password_provider.hash_password(password)
