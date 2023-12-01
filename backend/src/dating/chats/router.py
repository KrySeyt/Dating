from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, status, Body, Path, Query, HTTPException

from .exceptions import UserNotInChat, ChatNotFound
from .schema import ChatOut
from .service import ChatService
from ..dependencies import Stub, Dataclass
from ..messages.exceptions import MessageNotFound
from ..users.schema import User
from ..users.dependencies import get_current_user
from ..users.exceptions import UserNotFound
from ..messages.schema import MessageOut, MessageIn
from ..messages.service import MessageService


chats_router = APIRouter(tags=["Chats"], prefix="/chats")


@chats_router.get(
    "/my",
    response_model=list[ChatOut],
    tags=["Public"],
)
def get_my_chats(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        current_user: Annotated[User, Depends(get_current_user)],
        offset: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100,
) -> list[Dataclass]:

    try:
        chats = chat_service.get_user_chats(current_user.id, offset, limit)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [asdict(chat) for chat in chats]


@chats_router.get(
    "/{chat_id}",
    response_model=ChatOut,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def get_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        chat_id: Annotated[int, Path()],
) -> Dataclass:

    chat = chat_service.get_by_id(chat_id)

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(chat)


@chats_router.get(
    "/my/{chat_id}",
    response_model=ChatOut,
    tags=["Public"],
)
def get_my_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        current_user: Annotated[User, Depends(get_current_user)],
        chat_id: Annotated[int, Path()],
) -> Dataclass:

    chat = chat_service.get_by_id(chat_id)

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if current_user.id not in chat.users_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return asdict(chat)


@chats_router.get(
    "/user/{user_id}",
    response_model=list[ChatOut],
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def get_user_chats(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        user_id: Annotated[int, Path()],
        offset: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100,
) -> list[Dataclass]:

    try:
        chats = chat_service.get_user_chats(user_id, offset, limit)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [asdict(chat) for chat in chats]


@chats_router.get(
    "/{chat_id}/messages",
    response_model=list[MessageOut],
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def get_chat_messages(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        chat_id: Annotated[int, Path()],
        offset: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100,
) -> list[Dataclass]:

    try:
        messages_ids = chat_service.get_chat_messages_ids(chat_id, offset, limit)
        messages = message_service.get_messages_by_ids(messages_ids)
    except (ChatNotFound, MessageNotFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [asdict(message) for message in messages]


@chats_router.get(
    "/my/{chat_id}/messages",
    response_model=list[MessageOut],
    tags=["Public"],
)
def get_my_chat_messages(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        chat_id: Annotated[int, Path()],
        offset: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100,
) -> list[Dataclass]:

    chat = chat_service.get_by_id(chat_id)

    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    if current_user.id not in chat.users_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User has not permission for this chat")

    try:
        messages_ids = chat_service.get_chat_messages_ids(chat_id, offset, limit)
        messages = message_service.get_messages_by_ids(messages_ids)
    except (ChatNotFound, MessageNotFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    return [asdict(message) for message in messages]


@chats_router.post(
    "/",
    response_model=ChatOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def create_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        users_ids: Annotated[list[int], Body()],
) -> Dataclass:

    try:
        chat = chat_service.create_chat(users_ids=users_ids)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return asdict(chat)


@chats_router.post(
    "/start",
    response_model=ChatOut | None,
    status_code=status.HTTP_201_CREATED,
    tags=["Public"],
)
def create_chat_with_matched_user(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        current_user: Annotated[User, Depends(get_current_user)],
) -> Dataclass | None:

    chat = chat_service.create_chat_with_matched_user(current_user.id)
    return asdict(chat) if chat else None


@chats_router.post(
    "/send",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Public"],
)
def send_message_to_chat(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        message_in: Annotated[MessageIn, Body()],
) -> Dataclass:

    try:
        message = message_service.create(message_in, current_user.id)
    except ChatNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat doesn't exist")
    except UserNotInChat:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in chat")

    return asdict(message)


@chats_router.delete(
    "/{chat_id}",
    response_model=ChatOut,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def delete_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        chat_id: Annotated[int, Path()],
) -> Dataclass:

    try:
        chat = chat_service.delete_chat(chat_id)
    except ChatNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(chat)


@chats_router.delete(
    "/my/{chat_id}",
    response_model=ChatOut,
    tags=["Public"],
)
def delete_my_chat(
        chat_service: Annotated[ChatService, Depends(Stub(ChatService))],
        chat_id: Annotated[int, Path()],
        current_user: Annotated[User, Depends(get_current_user)],
) -> Dataclass:

    try:
        chat = chat_service.delete_chat_for_user(chat_id, current_user.id)
    except ChatNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(chat)
