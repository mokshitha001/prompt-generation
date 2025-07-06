from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import SessionLocal
from models.pydantic_models import UserCreate, UserLogin, UserResponse, PromptResponse
from models.orm_models import User, Prompt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model = UserResponse)
def create_user(user : UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.gmail_id == user.gmail_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        gmail_id = user.gmail_id,
        user_name = user.user_name,
        password = user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/users/verify", response_model=UserResponse)
def verify_login(credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.gmail_id == credentials.gmail_id).first()
    if not db_user or db_user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user

@router.get("/users/{gmail_id}/verify_credits")
def verify_credits(gmail_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.gmail_id == gmail_id).first()

    if user.credits < 10:
        raise HTTPException(status_code=403, detail="Insufficient credits")
    return user.credits



@router.get("/history/{gmail_id}", response_model=List[PromptResponse])
def get_user_chats(gmail_id: str, db: Session = Depends(get_db)):
    return db.query(Prompt).filter(Prompt.gmail_id == gmail_id).order_by(Prompt.timestamp.desc()).all()

@router.delete("/delete/{gmail_id}/{prompt_id}")
def delete_chat(gmail_id: str, prompt_id: int, db: Session = Depends(get_db)):
    chat = db.query(Prompt).filter(
        Prompt.id == prompt_id,
        Prompt.gmail_id == gmail_id
    ).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Prompt not found")

    db.delete(chat)
    db.commit()
    return {"message": "Prompt deleted successfully"}


