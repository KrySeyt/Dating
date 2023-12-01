from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, Query, HTTPException

from .exceptions import MessageNotFound
from .schema import MessageOut
from ..dependencies import Stub, Dataclass
from ..messages.service import MessageService
from ..users.dependencies import get_current_user
from ..users.exceptions import UserNotFound
from ..users.schema import User

messages_router = APIRouter(tags=["Messages"], prefix="/messages")


@messages_router.get(
    "/my/{message_id}",
    response_model=MessageOut,
    tags=["Public"],
)
def get_my_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        current_user: Annotated[User, Depends(get_current_user)],
        message_id: Annotated[int, Path()],
) -> Dataclass:

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
) -> Dataclass:

    message = message_service.get_by_id(message_id)

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if current_user.id != message.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    try:
        message = message_service.delete_message(message_id)
    except MessageNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

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
) -> list[Dataclass]:

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
) -> list[Dataclass]:

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
) -> Dataclass:

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
) -> Dataclass:

    try:
        message = message_service.delete_message(message_id)
    except MessageNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(message)
