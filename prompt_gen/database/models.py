from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    gmail_id = Column(String, primary_key=True, index=True, nullable=False)
    user_name = Column(String, nullable=False)
    credits = Column(Integer, default=100)
    subscription_status = Column(String, default="free")
    created_at = Column(DateTime, default=datetime.utcnow)

    chats = relationship("Chat", back_populates="user", cascade="all, delete")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String, ForeignKey("users.gmail_id", ondelete="CASCADE"))
    original_question = Column(Text, nullable=False)
    question_1 = Column(Text, nullable=False)
    question_2 = Column(Text, nullable=False)
    question_3 = Column(Text, nullable=False)
    question_4 = Column(Text, nullable=False)
    question_5 = Column(Text, nullable=False)
    original_answer = Column(Text, nullable=False)
    answer_1 = Column(Text, nullable=False)
    answer_2 = Column(Text, nullable=False)
    answer_3 = Column(Text, nullable=False)
    answer_4 = Column(Text, nullable=False)
    answer_5 = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")

