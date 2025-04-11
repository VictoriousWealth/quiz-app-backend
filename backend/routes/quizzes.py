from fastapi import APIRouter, Depends, HTTPException
from db.session import get_db
from sqlalchemy.orm import Session
from auth.utils import get_current_user
from db.models import User
from db.models import Quiz

router = APIRouter()

@router.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {
        "quiz_id": quiz.id,
        "created_at": quiz.created_at,
        "questions": [
            {
                "id": q.id,
                "text": q.text,
                "options": q.options,
            }
            for q in quiz.questions
        ]
    }
