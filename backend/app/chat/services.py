from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.pusher import pusher_client
from app.models import Conversation, Users
import datetime


async def create_conversation_db(
    db: Session, user: Users, recepient: Users
) -> Conversation:
    try:
        existing_conversation = (
            db.query(Conversation)
            .filter(
                and_(
                    Conversation.users.contains(user),
                    Conversation.users.contains(recepient),
                )
            )
            .first()
        )

        if existing_conversation:
            conversation = existing_conversation
        else:
            conversation = Conversation(created_at=datetime.datetime.utcnow(), updated_at=datetime.datetime.utcnow())
            conversation.users.append(user)
            conversation.users.append(recepient)
            db.add(conversation)
            db.commit()
            pusher_client.trigger(
                f"{user.mail}",
                "conversation:new",
                jsonable_encoder(conversation),
            )

    except Exception as exc_info:
        await db.rollback()
        raise exc_info

    else:
        return conversation
