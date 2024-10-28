from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session as get_db
from fastapi import APIRouter, Depends
from users.services import get_user_by_email

router = APIRouter(
    prefix="/users",
    tags=["Messaging"]
)


@router.get("/get_user", response_model=str)
async def get_user(email: str,
                   db: AsyncSession = Depends(get_db),
                   ):
    user = await get_user_by_email(email, db=db)
    return user.username
