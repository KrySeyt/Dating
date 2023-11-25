from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from passlib.ifc import PasswordHash

from .schema import UserIn, UserOut, User, LoginData
from .service import UserService
from .security import SESSION_EXPIRATION_TIME, SessionProvider
from .dependencies import get_current_user, get_session_id, get_user_in
from .exceptions import UserAlreadyExists
from ..dependencies import Stub, Dataclass


users_router = APIRouter(tags=["users"], prefix="/users")


@users_router.get("/me", response_model=UserOut)
def get_me(
        current_user: Annotated[User, Depends(get_current_user)]
) -> Dataclass:

    return asdict(current_user)


@users_router.get("/{user_id}", response_model=UserOut)
def get_user(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        user_id: int
) -> Dataclass:

    user = user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404)

    return asdict(user)


@users_router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        user_in: Annotated[UserIn, Depends(get_user_in)],
) -> Dataclass:

    try:
        user = user_service.register(user_in)
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return asdict(user)


@users_router.post("/login")
def login(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        session_provider: Annotated[SessionProvider, Depends(Stub(SessionProvider))],
        password_hasher: Annotated[PasswordHash, Depends(Stub(PasswordHash))],
        user_data: LoginData,
        response: Response,
) -> str:

    requested_user = user_service.get_user_by_username(user_data.username)

    if not requested_user:  # TODO: all this logic to specific components
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not password_hasher.verify(user_data.password, requested_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    session_id = session_provider.create_token(requested_user.id)
    response.set_cookie(key="Authorization", value=f"Basic {session_id}", expires=SESSION_EXPIRATION_TIME)

    return "success"


@users_router.post("/logout")
def logout(
        session_id: Annotated[str, Depends(get_session_id)],
        session_provider: Annotated[SessionProvider, Depends(Stub(SessionProvider))],
        response: Response,
) -> str:

    response.delete_cookie("Authorization")
    session_provider.expire_token(session_id)
    
    return "success"
