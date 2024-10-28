from messaging.schemas import MessageCreate
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Message, User
from sqlalchemy.orm import aliased


async def send_message(message_data: MessageCreate, db: AsyncSession):
    new_message = Message(
        sender_id=message_data.sender_id,
        recipient_id=message_data.recipient_id,
        content=message_data.content,
        timestamp=datetime.utcnow()
    )

    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    return new_message


async def get_messages_between_users(username: str,
                                     recipient: str,
                                     db: AsyncSession):
    sender_alias = aliased(User)
    recipient_alias = aliased(User)

    result = await db.execute(
        select(
            Message.id,
            sender_alias.username.label("sender_username"),
            recipient_alias.username.label("recipient_username"),
            Message.content,
            Message.timestamp
        )
        .join(sender_alias, Message.sender_id == sender_alias.id)
        .join(recipient_alias, Message.recipient_id == recipient_alias.id)
        .where(
            ((sender_alias.username == username) & (recipient_alias.username == recipient)) |
            ((sender_alias.username == recipient) & (recipient_alias.username == username))
        )
        .order_by(Message.timestamp)
    )

    messages = result.mappings().all()

    return messages


async def get_chat_partners(username: str, db: AsyncSession):
    user_result = await db.execute(select(User.id).where(User.username == username))
    user_id = user_result.scalar()

    result = await db.execute(
        select(User.username)
        .join(Message, (Message.sender_id == user_id) &
              (Message.recipient_id == User.id) |
              (Message.recipient_id == user_id) &
              (Message.sender_id == User.id))
        .where(User.id != user_id)
        .distinct()
    )

    partners = result.scalars().all()
    return partners
