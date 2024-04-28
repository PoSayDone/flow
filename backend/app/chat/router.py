import datetime
from operator import and_

from sqlalchemy import select
from fastapi.encoders import jsonable_encoder

from app.chat.services import create_conversation_db
from app.pusher import pusher_client
from sqlalchemy.orm import selectinload
from app import schema, models
from fastapi import APIRouter, Depends, HTTPException

from app.auth.services import user_dependency
from app.dependencies import db_dependency


chat_router = APIRouter(tags=["chats"])


@chat_router.get("/chats/")
async def get_user_chats(
    db: db_dependency,
    current_user: user_dependency,
):
    query = (
        select(models.Conversation)
        .where(
            and_(
                models.Conversation.users.contains(current_user),
                models.Conversation.is_deleted.is_(False),
            )
        )
        .options(selectinload(models.Conversation.users))
        .options(selectinload(models.Conversation.messages))
    ).order_by(models.Conversation.updated_at.desc())

    result = db.execute(query)

    chats: list[models.Conversation] = result.scalars().all()
    return chats


@chat_router.get("/chats/{conversation_id}")
async def get_chat_messages(
    conversation_id: int,
    db: db_dependency,
    user: user_dependency,
):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    conversation = (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conversation_id)
        .filter(models.Conversation.users.contains(user))
        .first()
    )
    if conversation:
        return {"messages": conversation.messages, "users": conversation.users}


@chat_router.post("/chats/create")
async def create_conversation(
    db: db_dependency,
    create_conversation_schema: schema.CreateConversation,
    user: user_dependency,
):
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")

    recepient = db.get(models.Users, create_conversation_schema.recipient_user_id)

    if not recepient:
        raise HTTPException(status_code=404, detail="Recepient not found")

    await create_conversation_db(db, user, recepient)


@chat_router.post("/chats/{conversation_id}")
async def send_message(
    conversation_id: int,
    new_message: schema.NewMessage,
    db: db_dependency,
    user: user_dependency,
):
    if not user:
        raise HTTPException(status_code=404, detail="Not authorized")
    existing_conversation: models.Conversation | None = db.query(
        models.Conversation
    ).get(conversation_id)
    if existing_conversation:
        message_obj = models.Message(
            conversation_id=conversation_id,
            sender_id=user.id,
            body=new_message.content,
            created_at=datetime.datetime.utcnow(),
        )
        db.add(message_obj)

        for user in existing_conversation.users:
            pusher_client.trigger(
                f"{user.mail}",
                "message:new",
                jsonable_encoder(message_obj),
            )
    else:
        raise HTTPException(status_code=400, detail="Invalid id")

    db.commit()
