from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    telegram_username: str
    telegram_chatid: Optional[int]
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    telegram_username: str
    password: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserLogin(schemas.BaseUser):
    username: str
    password: str
