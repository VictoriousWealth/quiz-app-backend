from fastapi import APIRouter, Depends, HTTPException
from auth.utils import get_current_user
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Quiz, UploadedFile, Question, User
from services.gemini_service import generate_additional_questions
import json
import fitz  # PyMuPDF
from docx import Document


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


@router.post("/dashboard/files/{file_id}/generate")
def generate_more_questions(file_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Fetch file
    file = db.query(UploadedFile).filter(UploadedFile.id == file_id, UploadedFile.user_id == current_user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = f"uploads/{file.filename}"
    try:
        if file.file_type == 'pdf':
            doc = fitz.open(file_path)
            full_text = "\n".join([page.get_text() for page in doc])
        elif file.file_type == 'docx':
            doc = Document(file_path)
            full_text = "\n".join([para.text for para in doc.paragraphs])
        else:  # .txt
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                full_text = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from {file.file_type}: {e}")


    # Get all existing questions for this file
    existing_questions = (
        db.query(Question.text)
        .join(Quiz)
        .filter(Quiz.file_id == file_id)
        .all()
    )
    existing_texts = [q.text for q in existing_questions]

    # Call Gemini with awareness of previous questions
    response_text = generate_additional_questions(full_text, existing_texts)

    try:
        questions_data = json.loads(response_text.strip("```json\n").strip("```"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini returned bad JSON: {e}")

    # Create new quiz section
    new_quiz = Quiz(file_id=file_id)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    for q in questions_data["questions"]:
        question = Question(
            quiz_id=new_quiz.id,
            text=q["question"],
            options=q["options"],
            correct_answer=q["answer"],
            explanation=q.get("explanation", "")
        )
        db.add(question)

    db.commit()

    return {"quiz_id": new_quiz.id, "section_number": len(existing_questions) // 5 + 1, "questions": questions_data["questions"]}
