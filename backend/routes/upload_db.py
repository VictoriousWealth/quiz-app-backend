from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os, uuid, json
from db.session import get_db
from db.models import UploadedFile, Quiz, Question
from services.gemini_service import generate_quiz_from_text
from auth.utils import get_current_user
from db.models import User
import docx
from docx.opc.exceptions import PackageNotFoundError
from fitz import open as open_pdf, FileDataError
import traceback

def extract_text_from_file(path, ext):
    ext = ext.lower()

    try:
        if ext == ".pdf":
            doc = open_pdf(path)
            text = "\n".join([page.get_text() for page in doc])
        elif ext == ".docx":
            doc = docx.Document(path)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:  # assume .txt
            with open(path, "r", encoding="utf-8", errors="strict") as f:
                text = f.read()
        
        if not text.strip():  # 💥 This is key
            raise HTTPException(status_code=400, detail="File is empty or contains no readable text.")
        
        return text

    except PackageNotFoundError:
        raise HTTPException(status_code=400, detail="Invalid or corrupted DOCX file.")
    except FileDataError:
        raise HTTPException(status_code=400, detail="Invalid or corrupted PDF file.")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid or non-text .txt file.")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to extract text: {str(e)}")

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", name="upload_file_and_generate_quiz")
async def upload_and_generate_quiz(
        file: UploadFile = File(...), 
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_user)
    ):
    # Store uploaded file
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return JSONResponse(status_code=415, content={"error": "Unsupported file type."})


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
    # response_text = generate_quiz_from_text(text, db)
    questions = await generate_quiz_from_text(text, db)


    quiz = Quiz(file_id=file_record.id)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    for q in questions:
        question = Question(
            id=q["id"],
            quiz_id=quiz.id,
            text=q["question"],
            options=q["options"],
            correct_answer=q["answer"],
            explanation=q.get("explanation", "No explanation provided.")
        )
        db.add(question)

    db.commit()
    return {"quiz_id": quiz.id, "questions": questions, "file_id": file_record.id}
