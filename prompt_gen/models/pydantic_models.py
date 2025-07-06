from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    gmail_id: str
    user_name: str
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    credits: int = 100

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    gmail_id: str
    password: str


    
class PromptCreate(BaseModel):
    gmail_id: str
    idea: str

class PromptAnswerInput(BaseModel):
    gmail_id: str
    answers: list[str]

class PromptResponse(BaseModel):
    id: int
    idea: str
    questions: str
    answers: str
    final_prompt: str
    timestamp: datetime

    class Config:
        from_attributes = True
