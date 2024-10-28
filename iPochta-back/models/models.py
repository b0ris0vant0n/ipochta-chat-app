from sqlalchemy import TIMESTAMP, Boolean
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    telegram_username = Column(String, unique=True, nullable=True)
    telegram_chatid = Column(Integer, unique=True, index=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    sent_messages = relationship("Message",
                                 foreign_keys="Message.sender_id",
                                 back_populates="sender")
    received_messages = relationship("Message",
                                     foreign_keys="Message.recipient_id",
                                     back_populates="recipient")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User",
                          foreign_keys=[sender_id],
                          back_populates="sent_messages")
    recipient = relationship("User",
                             foreign_keys=[recipient_id],
                             back_populates="received_messages")
