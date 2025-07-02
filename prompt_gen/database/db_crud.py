from sqlalchemy.orm import Session
from datetime import datetime
from models. models import User, Chat
from schemas import UserCreate, ChatCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        gmail_id=user.gmail_id,
        user_name=user.user_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, gmail_id: str):
    return db.query(User).filter(User.gmail_id == gmail_id).first()



def create_chat(db: Session, chat: ChatCreate):
    user = get_user(db, chat.gmail_id)
    db_chat = Chat(**chat.dict() )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_user_chats(db: Session, gmail_id: str):
    return db.query(Chat).filter(Chat.gmail_id == gmail_id).order_by(Chat.timestamp.desc()).all()

def delete_chat(db: Session, chat_id: int, gmail_id: str):
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.gmail_id == gmail_id
    ).first()
    if chat:
        db.delete(chat)
        db.commit()
    return chat

