from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.orm_models import Prompt, User
from database.db import SessionLocal
from models.pydantic_models import PromptCreate, PromptAnswerInput, PromptResponse
import openai, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/idea", response_model=PromptResponse)
def receive_idea(payload: PromptCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.gmail_id == payload.gmail_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    messages = [
        {"role": "system", "content": "You are an AI that helps improve user ideas by asking specific, personalized questions."},
        {"role": "user", "content": f"My idea: {payload.idea}. Please ask 5-10 questions to clarify and improve this idea."}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=messages
        )
        questions = response.choices[0].message["content"].strip().split("\n")
        question_text = "\n".join(questions)

        prompt_entry = Prompt(
            gmail_id=payload.gmail_id,
            idea=payload.idea,
            questions=question_text,
            answers="",
            final_prompt=""
        )
        db.add(prompt_entry)
        db.commit()
        db.refresh(prompt_entry)

        return prompt_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/answer", response_model=PromptResponse)
def receive_answers(payload: PromptAnswerInput, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.gmail_id == payload.gmail_id).order_by(Prompt.timestamp.desc()).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt entry not found")

    the_user_gmail_id = prompt.gmail_id
    the_user = db.query(User).filter(User.gmail_id == the_user_gmail_id).first()
    the_user.credits -= 10
    db.commit()

    answers_text = "\n".join(payload.answers)

    messages = [
        {"role": "system", "content": "You are an expert prompt engineer."},
        {"role": "user", "content": f"""The user has this idea: {prompt.idea}.
Here are their detailed responses: {answers_text}.
Generate a clear, reusable AI prompt  that can be given to an LLM to produce a high-quality, detailed output on this topic."""}
]
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=messages
        )
        refined_prompt = response.choices[0].message["content"]

        prompt.answers = answers_text
        prompt.final_prompt = refined_prompt
        db.commit()
        db.refresh(prompt)

        return prompt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
