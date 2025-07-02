from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.db_crud import get_user, create_user, create_chat, get_user_chats, delete_chat 
from database.schemas import UserCreate, UserResponse, ChatCreate, ChatResponse
from database.db_connect import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model = UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.gmail_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(db, user)

@router.get("/users/{gmail_id}", response_model = UserResponse)
def get_user_route(gmail_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, gmail_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/chats/", response_model = ChatResponse)
def create_chat_route(chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = create_chat(db, chat)
    if db_chat is None:
        raise HTTPException(status_code=403, detail="User not found or insufficient credits")
    return db_chat

@router.get("/chats/{gmail_id}", response_model = List[ChatResponse])
def get_chats_route(gmail_id: str, db: Session = Depends(get_db)):
    return get_user_chats(db, gmail_id)

@router.delete("/chats/{gmail_id}/{chat_id}")
def delete_chat_route(gmail_id: str, chat_id: int, db: Session = Depends(get_db)):
    chat = delete_chat(db, chat_id, gmail_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}

