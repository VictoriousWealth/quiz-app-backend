# ⚙️ Backend – FastAPI + Gemini AI

This is the backend API service for the Gemini-powered Quiz App.

---

## Purpose
FastAPI backend that handles file uploads, integrates with Gemini, stores quizzes/results, and serves the frontend.

--- 

## ✅ Features Implemented

- Upload `.pdf`, `.docx`, and `.txt` files
- File validation & rejection of unsupported types
- Permanent file storage in `/uploads/`
- Text extraction from files (PDF: PyMuPDF, DOCX: python-docx)
- Gemini AI integration to:
  - Generate quizzes from uploaded content
  - Evaluate user answers with feedback + correctness
- CORS-enabled for frontend (localhost:3000)

--- 

## 🛠️ Running the Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```
---
## 📂 File Structure

```bash
`backend`
├── `main.py`               # FastAPI app + CORS
├── `routes`
│   ├── `answers.py`        # Quiz answer checking via Gemini
│   └── `upload.py`         # File upload + Gemini quiz generation
├── `services`
│   └── `gemini_service.py` # Gemini prompt logic
├── `uploads`               # Saved uploaded files
├── `.env`                  # Contains GEMINI_API_KEY
```
--- 

## 🔐 Environment Setup
`.env` file:
```bash
GEMINI_API_KEY=your_api_key_here
```
---

## 🚧 Coming Next

- 📦 Database integration to track:
    - Uploads
    - Quiz results
    - User answers
- 🧠 Improved prompt formatting
- 🗃️ Admin dashboard

---


## Dependencies

- FastAPI
- Uvicorn
- python-multipart
- Google Gemini SDK (or REST-based request handler)

--- 

## Related Docs

- [Data Flow](../docs/architecture/data_flow.md)
- [API Design](../docs/architecture/api_design.md)

--- 









