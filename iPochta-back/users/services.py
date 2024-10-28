from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User


async def get_user_by_username(username: str, db: AsyncSession):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user


async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user


async def save_chat_id(chat_id: int, username: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.telegram_username == username))
    user = result.scalars().one_or_none()

    if user:
        user.telegram_chatid = chat_id
        await db.commit()
        await db.refresh(user)
        return user
