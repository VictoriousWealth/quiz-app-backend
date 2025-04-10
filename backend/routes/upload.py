import os
import fitz  # PyMuPDF
import docx
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import json
import re
from services.gemini_service import generate_quiz_from_text

router = APIRouter()

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(path):
    with open(path, 'r', encoding="utf-8", errors="ignore") as f:
        return f.read()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    # 🔒 Restrict allowed file types
    allowed_extensions = [".pdf", ".docx", ".txt"]
    if ext not in allowed_extensions:
        return JSONResponse(status_code=400, content={
            "error": "Unsupported file format. Only PDF, DOCX, and TXT files are allowed."
        })

    file_location = f"/tmp/{filename}"

    # Save file to disk
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Extract text based on file type
    if ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_location)
    elif ext == ".docx":
        extracted_text = extract_text_from_docx(file_location)
    elif ext == ".txt":
        extracted_text = extract_text_from_txt(file_location)

    # ... rest of your Gemini + JSON logic continues

    print("EXTRACTED TEXT:", extracted_text[:500])

    gemini_response = generate_quiz_from_text(extracted_text)

    # Clean and parse JSON from Gemini
    match = re.search(r"```json\n(.*?)```", gemini_response, re.DOTALL)
    cleaned_json = match.group(1) if match else gemini_response.strip()

    try:
        quiz = json.loads(cleaned_json)
    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
        return JSONResponse(status_code=500, content={"error": "Invalid response from Gemini."})

    return JSONResponse(content=quiz)
