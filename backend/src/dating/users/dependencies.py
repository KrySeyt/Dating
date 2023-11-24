from typing import Annotated, Type
from dataclasses import asdict

from fastapi import Depends, HTTPException, status, Request
from passlib.ifc import PasswordHash

from .schema import User, RawUserIn, UserIn
from .service import UserService
from .security import SessionProvider, AuthenticationError
from ..dependencies import Stub


def get_session_id(request: Request) -> str:
    auth_cookie = request.cookies.get("Authorization")

    if not auth_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    _, session_id = auth_cookie.split()
    return session_id


def get_current_user(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        session_provider: Annotated[SessionProvider, Depends(Stub(SessionProvider))],
        session_id: Annotated[str, Depends(get_session_id)]
) -> User:

    try:
        user_id = session_provider.validate_token(session_id)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return user


def get_user_in(
        password_hasher: Annotated[Type[PasswordHash], Depends(Stub(PasswordHash))],
        raw_user: RawUserIn
) -> UserIn:
    user_data = asdict(raw_user)
    user_data["hashed_password"] = password_hasher.hash(user_data.pop("password"))
    return UserIn(**user_data)
