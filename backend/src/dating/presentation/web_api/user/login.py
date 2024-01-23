from typing import Annotated

from fastapi import Depends, Body, Response, status, HTTPException

from dating.adapters.database.exceptions import UserNotFound
from dating.application.user.login import LoginDTO, WrongCredentials
from .router import user_router
from ...interactor_factory.user import UserInteractorFactory


@user_router.post("/login")
def login(
        interactor_factory: Annotated[UserInteractorFactory, Depends()],
        response: Response,
        username: Annotated[str, Body(embed=True)],
        password: Annotated[str, Body(embed=True)],
) -> None:
    try:
        with interactor_factory.login() as login_interactor:
            token = login_interactor(LoginDTO(
                username=username,
                password=password,
            ))
    except (UserNotFound, WrongCredentials):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    response.set_cookie("Authorization", value=rf"basic {token}")

