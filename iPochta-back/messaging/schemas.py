from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    sender_id: int
    recipient_id: int
    content: str


class Message(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True


class Messages(BaseModel):
    id: int
    sender_username: str
    recipient_username: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
