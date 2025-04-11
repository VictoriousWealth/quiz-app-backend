from fastapi import APIRouter, Depends
from auth.utils import get_current_user
from db.models import User
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Quiz
from db.models import UploadedFile
from db.models import Question

router = APIRouter()


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}


@router.get("/dashboard")
def get_user_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quizzes = (
        db.query(Quiz)
        .join(UploadedFile)
        .filter(UploadedFile.user_id == current_user.id)
        .all()
    )
    
    results = []
    for quiz in quizzes:
        results.append({
            "quiz_id": quiz.id,
            "file_name": quiz.file.original_name,
            "created_at": quiz.created_at,
            "question_count": len(quiz.questions),
        })
    
    return results

@router.get("/dashboard/files")
def get_user_files(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    files = db.query(UploadedFile).filter(UploadedFile.user_id == current_user.id).all()
    return files

@router.get("/dashboard/files/{file_id}/sections")
def get_sections(file_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quizzes = db.query(Quiz).filter(Quiz.file_id == file_id).all()
    data = []
    for i, quiz in enumerate(quizzes):
        questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
        data.append({
            "section_number": i + 1,
            "questions": questions
        })
    return data
