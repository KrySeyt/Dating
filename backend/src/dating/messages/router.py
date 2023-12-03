from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, Query, HTTPException, Body

from .exceptions import MessageNotFound
from .schema import MessageOut, MessageIn, MessageHideOut
from ..chats.exceptions import ChatNotFound, ChatUnavailableForUser
from ..dependencies import Stub, DataclassAsDict
from ..messages.service import MessageService
from ..users.dependencies import get_current_user
from ..users.exceptions import UserNotFound
from ..users.schema import User


messages_router = APIRouter(tags=["Messages"], prefix="/messages")


@messages_router.post(
    "/hide/{message_id}/chat/{chat_id}/user/{user_id}",
    response_model=MessageHideOut,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def hide_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        user_id: Annotated[int, Path()],
        chat_id: Annotated[int, Path()],
        message_id: Annotated[int, Path()],
) -> DataclassAsDict:

    try:
        hide = message_service.hide_message(message_id, chat_id, user_id)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except MessageNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    except ChatNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    return asdict(hide)


@messages_router.post(
    "/hide/{message_id}/chat/{chat_id}",
    response_model=MessageHideOut,
    tags=["Public"],
)
def hide_message_in_my_chat(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        chat_id: Annotated[int, Path()],
        message_id: Annotated[int, Path()],
) -> DataclassAsDict:

    try:
        hide = message_service.hide_message(message_id, chat_id, current_user.id)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except MessageNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    except ChatNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")

    return asdict(hide)


@messages_router.get(
    "/my/{message_id}",
    response_model=MessageOut,
    tags=["Public"],
)
def get_my_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        message_id: Annotated[int, Path()],
) -> DataclassAsDict:

    message = message_service.get_by_id(message_id)

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if current_user.id != message.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return asdict(message)


@messages_router.delete(
    "/my/{message_id}",
    response_model=MessageOut,
    tags=["Public"],
)
def delete_my_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        message_id: Annotated[int, Path()],
) -> DataclassAsDict:

    message = message_service.get_by_id(message_id)

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found1")

    if current_user.id != message.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    try:
        message = message_service.delete_message(message_id)
    except MessageNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found2")

    return asdict(message)


@messages_router.get(
    "/user/{user_id}",
    response_model=list[MessageOut],
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def get_user_messages(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        user_id: Annotated[int, Path()],
        offset: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100,
) -> list[DataclassAsDict]:

    try:
        messages = message_service.get_user_messages(user_id, offset, limit)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [asdict(message) for message in messages]


@messages_router.get(
    "/my",
    response_model=list[MessageOut],
    tags=["Public"],
)
def get_my_messages(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        offset: Annotated[int, Query()] = 0,
        limit: Annotated[int, Query()] = 100,
) -> list[DataclassAsDict]:

    try:
        messages = message_service.get_user_messages(current_user.id, offset, limit)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [asdict(message) for message in messages]


@messages_router.get(
    "/{message_id}",
    response_model=MessageOut,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def get_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        message_id: Annotated[int, Path()],
) -> DataclassAsDict:

    message = message_service.get_by_id(message_id)

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(message)


@messages_router.delete(
    "/{message_id}",
    response_model=MessageOut,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services",
)
def delete_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        message_id: Annotated[int, Path()],
) -> DataclassAsDict:

    try:
        message = message_service.delete_message(message_id)
    except MessageNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(message)


@messages_router.post(
    "",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Public"],
)
def create_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        message_in: Annotated[MessageIn, Body()],
) -> DataclassAsDict:

    try:
        message = message_service.create(message_in, current_user.id)
    except ChatNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat doesn't exist")
    except ChatUnavailableForUser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in chat")

    return asdict(message)
