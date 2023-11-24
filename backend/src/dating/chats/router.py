from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, status, Body

from .schema import ChatOut
from .service import ChatService
from ..dependencies import Stub, Dataclass
from ..users.schema import User
from ..users.dependencies import get_current_user


chats_router = APIRouter(tags=["chats"], prefix="/chats")


@chats_router.post("/", response_model=ChatOut, status_code=status.HTTP_201_CREATED)
def create_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        current_user: Annotated[User, Depends(get_current_user)],
        users_ids: Annotated[list[int], Body()],
) -> Dataclass:

    chat = chat_service.create_chat(users_ids=(current_user.id, *users_ids))
    return asdict(chat)
