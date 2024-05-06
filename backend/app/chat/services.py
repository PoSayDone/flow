from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.pusher import pusher_client
from app.models import Conversation, Users
from datetime import UTC, datetime


async def create_conversation_db(
    db: Session, user: Users, recepient: Users
) -> Conversation:
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
        conversation = Conversation(
            # created_at=datetime.now(UTC),
            # updated_at=datetime.now(UTC),
        )
        conversation.users.append(user)
        conversation.users.append(recepient)
        db.add(conversation)
        db.commit()
        pusher_client.trigger(
            f"{user.mail}",
            "conversation:new",
            jsonable_encoder(conversation),
        )

    return conversation
