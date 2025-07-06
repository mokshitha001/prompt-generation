from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class User(Base):
    __tablename__ = "users"

    gmail_id = Column(String, primary_key=True, index=True)
    user_name = Column(String)
    password = Column(String)
    credits = Column(Integer, default=100)

    prompts = relationship("Prompt", back_populates="user", cascade="all, delete")


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String, ForeignKey("users.gmail_id", ondelete="CASCADE"))
    idea = Column(Text)
    questions = Column(Text)  
    answers = Column(Text)   
    final_prompt = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="prompts")

