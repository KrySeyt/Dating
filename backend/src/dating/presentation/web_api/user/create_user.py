from typing import Annotated

from fastapi import Depends, Body

from dating.application.user.create_user import NewUserDTO, CreatedUserDTO
from .router import user_router
from ..dependencies.user import get_hashed_password
from ...interactor_factory.user import UserInteractorFactory


@user_router.post(r"/")
def create_user(
        interactor_factory: Annotated[UserInteractorFactory, Depends()],
        username: Annotated[str, Body(embed=True)],
        hashed_password: Annotated[str, Depends(get_hashed_password)],
) -> CreatedUserDTO:
    with interactor_factory.create_user() as create_user_interactor:
        return create_user_interactor(NewUserDTO(
            username=username,
            hashed_password=hashed_password,
        ))
