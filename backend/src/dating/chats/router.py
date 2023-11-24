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


@chats_router.post(
    "/",
    response_model=ChatOut,
    status_code=status.HTTP_201_CREATED,
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

