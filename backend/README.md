
# 🧠 Backend (FastAPI)

## Purpose
FastAPI backend that handles file uploads, integrates with Gemini, stores quizzes/results, and serves the frontend.

## How to Run
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Dependencies

- FastAPI
- Uvicorn
- python-multipart
- Google Gemini SDK (or REST-based request handler)

## Related Docs

- [Data Flow](./architecture/data_flow.md)
- [API Design](./architecture/api_design.md)
