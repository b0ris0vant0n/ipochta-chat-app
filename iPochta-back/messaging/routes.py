from typing import List

from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import get_async_session as get_db
from fastapi import APIRouter, Depends

from auth.manager import get_user_manager
from messaging.services import get_messages_between_users
from messaging.schemas import Messages
from auth.database import User
from messaging.services import get_chat_partners

router = APIRouter(
    prefix="/messaging",
    tags=["Messaging"]
)

fastapi_user = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_user.current_user()


@router.get("/partners", response_model=List[str])
async def get_user_partners(db: AsyncSession = Depends(get_db),
                            user: User = Depends(current_user)):
    partners = await get_chat_partners(username=user.username, db=db)
    return partners


@router.get("/messages/history/{recipient}", response_model=List[Messages])
async def get_chat_history(recipient: str,
                           db: AsyncSession = Depends(get_db),
                           user: User = Depends(current_user)
                           ):
    messages = await get_messages_between_users(user.username, recipient, db)
    return messages
