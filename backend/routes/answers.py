from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from services.gemini_service import evaluate_answers
from db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from auth.utils import get_current_user
from models import User
from auth.utils import get_current_user

router = APIRouter()

@router.post("/")
async def check_answers(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await request.json()
    quiz_data = data.get("quizData")
    user_answers = data.get("userAnswers")

    try:
        result = evaluate_answers(quiz_data, user_answers)
        return JSONResponse(content=result)
    except Exception as e:
        print("Gemini answer evaluation failed:", e)
        return JSONResponse(status_code=500, content={"error": "Failed to evaluate answers."})
