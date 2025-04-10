# backend/routes/upload_db.py

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os, uuid, json
from db.session import get_db
from db.models import UploadedFile, Quiz, Question
from services.gemini_service import generate_quiz_from_text
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_and_generate_quiz(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Store uploaded file
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_record = UploadedFile(
        user_id="11111111-1111-1111-1111-111111111111",
        filename=filename,
        original_name=file.filename,
        file_type=ext.lower().lstrip(".")
    )
    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    # Get text content from file
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Get quiz JSON from Gemini
    response_text = generate_quiz_from_text(text)

    try:
        match = json.loads(response_text.strip("```json\n").strip("```"))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Gemini returned bad JSON: {e}"})

    # Save quiz and questions
    quiz = Quiz(file_id=file_record.id)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    for q in match["questions"]:
        question = Question(
            quiz_id=quiz.id,
            text=q["question"],
            options=q["options"]
        )
        db.add(question)

    db.commit()

    return {"quiz_id": quiz.id, "questions": match["questions"]}
