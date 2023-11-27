from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException

from .schema import MessageOut
from ..dependencies import Stub, Dataclass
from ..messages.service import MessageService


messages_router = APIRouter(tags=["Messages"], prefix="/messages")


@messages_router.get("/{message_id}", response_model=MessageOut)
def get_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        message_id: Annotated[int, Path()],
) -> Dataclass:

    message = message_service.get_by_id(message_id)

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(message)


@messages_router.get("/user/{user_id}", response_model=list[MessageOut])
def get_user_messages(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        user_id: Annotated[int, Path()],
) -> list[Dataclass]:

    messages = message_service.get_user_messages(user_id)

    if messages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [asdict(message) for message in messages]


@messages_router.delete(
    "/{message_id}",
    response_model=MessageOut,
    tags=["Non-public"],
    description="This endpoint should not be public. Hide it in nginx config. This only for use "
                "from another internal services"
)
def delete_message(
        message_service: Annotated[MessageService, Depends(Stub(MessageService))],
        message_id: Annotated[int, Path()],
) -> Dataclass:

    message = message_service.delete_message(message_id)

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(message)


# @messages_router.delete("/my/{message_id}", response_model=MessageOut)
# def delete_my_message(
#         message_service: Annotated[MessageService, Depends(Stub(MessageService))],
#         current_user: Annotated[User, Depends(get_current_user)],
#         message_id: Annotated[int, Path()],
# ) -> Dataclass:
#
#     message = message_service.delete_message_for_user(message_id, current_user.id)
#
#     if not message:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
#     return asdict(message)
