from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from services.gemini_service import evaluate_answers
from db.session import get_db
from sqlalchemy.orm import Session
from auth.utils import get_current_user
from db.models import User, QuizAttempt, UserAnswer

router = APIRouter()

@router.post("/")
async def check_answers(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = await request.json()
    quiz_data = data.get("quizData")
    user_answers = data.get("userAnswers")
    
    if not isinstance(user_answers, (list, dict)):
        raise HTTPException(status_code=422, detail="userAnswers must be a list.")


    # ✅ First, evaluate the result
    try:
        result = evaluate_answers(quiz_data, user_answers)
    except Exception as e:
        print("Gemini answer evaluation failed:", e)
        return JSONResponse(status_code=500, content={"error": "Failed to evaluate answers."})

    # ✅ Then store attempt
    attempt = QuizAttempt(user_id=current_user.id, quiz_id=quiz_data["quiz_id"], score=0)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # ✅ Save each answer and calculate score
    score = 0
    for question_result in result["results"]:
        raw_is_correct = question_result["is_correct"]

        if raw_is_correct is True:
            is_correct = True
        elif raw_is_correct is False:
            is_correct = False
        else:
            is_correct = None  # Catch cases like "Unknown" or any string

        if is_correct:
            score += 1

        db.add(UserAnswer(
            user_id=current_user.id,
            attempt_id=attempt.id,
            question_id=question_result["id"],
            answer=question_result["user_answer"],
            is_correct=is_correct
        ))

    # ✅ Update score in QuizAttempt
    attempt.score = score
    db.commit()

    return JSONResponse(content=result)
