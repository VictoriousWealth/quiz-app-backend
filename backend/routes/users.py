from fastapi import APIRouter, Depends, HTTPException
from auth.utils import get_current_user
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Quiz, UploadedFile, Question, User, QuizAttempt
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
            "quiz_id": quiz.id,
            "questions": questions
        })
    return data


@router.post("/dashboard/files/{file_id}/generate")
def generate_more_questions(file_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                full_text = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from {file.file_type}: {e}")

    existing_questions = (
        db.query(Question.text)
        .join(Quiz)
        .filter(Quiz.file_id == file_id)
        .all()
    )
    existing_texts = [q.text for q in existing_questions]

    response_text = generate_additional_questions(full_text, existing_texts)

    try:
        questions_data = json.loads(response_text.strip("```json\n").strip("```"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini returned bad JSON: {e}")

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

@router.get("/dashboard/history")
def get_quiz_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    all_attempts = (
        db.query(QuizAttempt)
        .join(Quiz)
        .join(UploadedFile)
        .filter(QuizAttempt.user_id == current_user.id)
        .order_by(QuizAttempt.submitted_at.desc())
        .all()
    )

    # Store only the latest attempt per quiz
    latest_attempts_by_quiz = {}
    for attempt in all_attempts:
        if attempt.quiz_id not in latest_attempts_by_quiz:
            latest_attempts_by_quiz[attempt.quiz_id] = attempt

    history = []

    for attempt in latest_attempts_by_quiz.values():
        quiz = db.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
        if not quiz:
            continue

        file = db.query(UploadedFile).filter(UploadedFile.id == quiz.file_id).first()
        if not file:
            continue

        # Determine section number
        all_quizzes_for_file = (
            db.query(Quiz).filter(Quiz.file_id == file.id).order_by(Quiz.created_at.asc()).all()
        )
        section_number = next((i + 1 for i, q in enumerate(all_quizzes_for_file) if q.id == quiz.id), None)

        num_questions = len(quiz.questions)
        label = f"{file.original_name} - Section {section_number}"

        history.append({
            "quiz_id": quiz.id,  # still useful for fetching attempts
            "label": label,
            "score": attempt.score,
            "submitted_at": attempt.submitted_at,
            "num_questions": num_questions
        })

    return history

@router.get("/dashboard/quiz/{quiz_id}/attempts")
def get_quiz_attempts(quiz_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get all attempts for this quiz by the current user
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.quiz_id == quiz_id
    ).order_by(QuizAttempt.submitted_at.desc()).all()

    # Fetch the quiz and associated file
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    file = db.query(UploadedFile).filter(UploadedFile.id == quiz.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Determine section number
    all_quizzes_for_file = (
        db.query(Quiz).filter(Quiz.file_id == file.id).order_by(Quiz.created_at.asc()).all()
    )
    section_number = next((i + 1 for i, q in enumerate(all_quizzes_for_file) if q.id == quiz.id), None)

    num_questions = len(quiz.questions)
    label = f"{file.original_name} - Section {section_number}"

    return [
        {
            "label": label,
            "score": a.score,
            "submitted_at": a.submitted_at,
            "num_questions": num_questions
        }
        for a in attempts
    ]
