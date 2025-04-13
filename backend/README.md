# 🧠 Backend – AI-Powered Quiz Web App

This is the **FastAPI backend** for the AI-powered quiz generation platform. It handles user authentication, file uploads, quiz generation using Gemini AI, answer evaluation, history tracking, and more.

---

## 🚀 Tech Stack

- **FastAPI** (with Starlette and Pydantic)
- **SQLAlchemy** (ORM with PostgreSQL)
- **Alembic** for database migrations
- **Google Gemini API** for AI-powered quiz generation
- **UUID-based models** for secure record identification
- **JWT Authentication**

---

## 📁 Folder Structure

```
backend/
├── alembic/            # Migration scripts
├── auth/               # Login, password hashing, token generation
├── db/                 # Database models and session management
├── routes/             # API routes: answers, quizzes, uploads, users
├── services/           # Gemini AI service logic
├── tests/              # Pytest-based test suite
├── uploads/            # Uploaded files (PDF, DOCX, TXT)
├── main.py             # App entry point
├── alembic.ini         # Alembic config
├── requirements.txt    # Backend dependencies
```

---

## 🔐 Authentication

- JWT tokens are issued on login via `/auth/login`
- Token is passed in the header: `Authorization: Bearer <token>`
- Authenticated endpoints use FastAPI `Depends` to extract and verify tokens

---

## 📂 API Endpoints (Key Routes)

| Method | Path                        | Description                                  |
|--------|-----------------------------|----------------------------------------------|
| POST   | `/auth/register`           | Register a new user                          |
| POST   | `/auth/login`              | Log in and receive JWT token                 |
| POST   | `/upload-db/`              | Upload a document (PDF, DOCX, TXT)           |
| POST   | `/quizzes/generate/`       | Trigger Gemini to generate quiz questions    |
| POST   | `/answers/`                | Submit answers and receive evaluation        |
| GET    | `/dashboard`               | Get user-specific uploaded files/quizzes     |
| GET    | `/dashboard/files/{id}`    | Get quizzes per uploaded file                |
| GET    | `/history`                 | View latest attempt for each quiz            |
| GET    | `/history/{quiz_id}`       | View all attempts for a quiz                 |

---

## 🧠 AI Integration

- Uses **Google Gemini** via `services/gemini_service.py`
- Prompt engineering done in `ai_prompts/gemini_prompts.py`
- All quizzes include: `question`, `options[]`, `correct answer`, and `explanation`

---

## 🧪 Testing

Tests are located in `backend/tests/` and use **Pytest**

### ✅ Covered
- Auth flows
- Upload validations (PDF/DOCX/TXT only)
- Quiz submission and scoring
- Dashboard and history fetch
- Edge cases (e.g., empty files, bad JSON, invalid quiz attempts)

### Run tests:
```bash
cd backend
pytest
```

---

## ⚙️ Setup Instructions

### 1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set environment variables in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/quizdb
GEMINI_API_KEY=your_google_gemini_key
SECRET_KEY=your_jwt_secret_key
```

### 4. Run migrations:
```bash
alembic upgrade head
```

### 5. Start backend:
```bash
uvicorn main:app --reload
```

---

## 📌 Notes

- Gemini-generated quizzes are stored per file per user
- Each quiz has multiple attempts tracked
- UUIDs ensure secure and unique identification
- CORS enabled for frontend at `http://localhost:3000`

---

## 🌟 Example Prompts
See `ai_prompts/` for detailed prompt templates sent to Gemini API.

---

## 📄 License
MIT License

---

## 📬 Contact
Built with 💙 by [Nick Efe Oni](mailto:efeoni10@gmail.com).

Feel free to fork, star, and share your feedback!

## ✍️ Author

**Nick Efe Oni**  
[GitHub](https://github.com/VictoriousWealth) • [LinkedIn](https://www.linkedin.com/in/nick-efe-oni)  
✉️ [efeoni10@gmail.com](mailto:efeoni10@gmail.com)
