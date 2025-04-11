from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os, uuid, json
from db.session import get_db
from db.models import UploadedFile, Quiz, Question
from services.gemini_service import generate_quiz_from_text
from auth.utils import get_current_user
from db.models import User
import fitz  # PyMuPDF
import docx

def extract_text_from_file(path, ext):
    if ext == ".pdf":
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    elif ext == ".docx":
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:  # assume .txt
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_and_generate_quiz(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Store uploaded file
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    

    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_record = UploadedFile(
        user_id=current_user.id,
        filename=filename,
        original_name=file.filename,
        file_type=ext.lower().lstrip(".")
    )
    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    # Get text content from file
    text = extract_text_from_file(file_path, ext)

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
