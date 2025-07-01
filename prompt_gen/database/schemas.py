from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    gmail_id: str
    user_name: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    credits: int = 100
    subscription_status: str = "free"
    created_at: datetime

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    gmail_id: str
    original_question: str
    question_1: str
    question_2: str
    question_3: str
    question_4: str
    question_5: str
    original_answer: str
    answer_1: str
    answer_2: str
    answer_3: str
    answer_4: str
    answer_5: str

class ChatCreate(ChatBase):
    pass

class ChatResponse(ChatBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

