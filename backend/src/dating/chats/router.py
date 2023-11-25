from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, status, Body, Path, HTTPException

from .schema import ChatOut
from .service import ChatService
from ..dependencies import Stub, Dataclass
from ..users.schema import User
from ..users.dependencies import get_current_user
from ..users.exceptions import UserNotFound


chats_router = APIRouter(tags=["chats"], prefix="/chats")


@chats_router.get("/{chat_id}", response_model=ChatOut)
def get_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        chat_id: Annotated[int, Path()],
) -> Dataclass:

    chat = chat_service.get_by_id(chat_id)

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(chat)


@chats_router.get("/user/{user_id}", response_model=list[ChatOut])
def get_user_chats(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        user_id: Annotated[int, Path()],
) -> list[Dataclass]:

    chats = chat_service.get_user_chats(user_id)
    return [asdict(chat) for chat in chats]


@chats_router.post(
    "/",
    response_model=ChatOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services"
)
def create_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        current_user: Annotated[User, Depends(get_current_user)],
        users_ids: Annotated[list[int], Body()],
) -> Dataclass:

    try:
        chat = chat_service.create_chat(users_ids=(current_user.id, *users_ids))
    except UserNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    return asdict(chat)


@chats_router.post(
    "/start",
    response_model=ChatOut | None,
    status_code=status.HTTP_201_CREATED,
)
def create_chat_with_matched_user(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        current_user: Annotated[User, Depends(get_current_user)],
) -> Dataclass | None:

    chat = chat_service.create_chat_with_matched_user(current_user.id)
    return asdict(chat) if chat else None


@chats_router.delete(
    "/{chat_id}",
    response_model=ChatOut,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services"
)
def delete_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        chat_id: Annotated[int, Path()],
) -> Dataclass:

    chat = chat_service.delete_chat(chat_id)

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(chat)


@chats_router.delete("/my/{chat_id}", response_model=ChatOut)
def delete_my_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        chat_id: Annotated[int, Path()],
        current_user: Annotated[User, Depends(get_current_user)],
) -> Dataclass:

    chat = chat_service.delete_chat_for_user(chat_id, current_user.id)

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(chat)
