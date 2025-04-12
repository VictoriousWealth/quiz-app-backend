# AI-Powered Quiz Web App

Welcome to the **AI-Powered Quiz Web App**, a full-stack web application that transforms any uploaded document into an interactive quiz using Google's **Gemini AI**. Users can upload PDF, DOCX, or TXT files, take generated quizzes, and receive instant feedback, all within a modern, responsive interface.

---

## 🌟 Features

- 📄 **Smart Uploads**: Upload PDF, DOCX, or TXT files.
- 🤖 **AI Quiz Generation**: Uses Gemini AI to generate accurate multiple-choice questions.
- 🧠 **Instant Feedback**: Get answers and explanations right after quiz submission.
- 🗂 **Progress Tracking**: View quiz history and reattempt previous quizzes.
- 🔒 **JWT Authentication**: Secure signup/login with protected routes.
- 🌗 **Dark Mode**: Full dark/light theme support.

---

## 🧠 Tech Stack

| Layer      | Technology                             |
|------------|----------------------------------------|
| Frontend   | React.js, Bootstrap                    |
| Backend    | FastAPI, SQLAlchemy, Alembic           |
| AI         | Gemini API (Google's Generative AI)    |
| Database   | PostgreSQL                             |
| Auth       | JWT                                    |

---

## 📁 Project Structure

```
quiz-app/
├── backend/         # FastAPI + SQLAlchemy backend
│   ├── auth/        # JWT logic
│   ├── db/          # Models & DB session
│   ├── routes/      # All API endpoints
│   ├── services/    # AI Integration
│   └── tests/       # Full test suite
│
├── frontend/        # React frontend
│   ├── src/components/  # UI components
│   └── src/api/         # Axios instance
│
├── ai_prompts/      # Gemini prompt engineering
├── docs/            # Architecture + user stories
└── README.md
```

---

## 🛠️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/quiz-app.git
cd quiz-app
```

### 2. Set Up Environment Variables
Create a `.env` file inside the `backend/` folder:
```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
GEMINI_API_KEY=your_api_key
SECRET_KEY=your_jwt_secret
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

### 4. Frontend Setup
```bash
cd ../frontend
npm install
npm start
```

Now visit `http://localhost:3000` to start using the app!

---

## 🔍 Deployment
Deployment instructions for platforms like **Render**, **Vercel**, or **Heroku** will be provided soon. This MVP is almost ready for production.

---

## 📸 Demo & Screenshots
44 detailed screenshots will be uploaded to showcase user flow, dark/light mode, quiz results, and dashboard views. *(Coming Soon)*

---

## 💡 Future Enhancements
- Admin dashboard
- Shareable quiz links
- Custom quiz generation settings
- Gamification elements (badges, leaderboard)

---

## 🧪 Tests
```bash
cd backend
pytest tests/
```
Covers: login edge cases, quiz generation, file uploads, dashboard queries, and answer checking.

---

## 📄 License
MIT License

---

## 🙌 Acknowledgements
- [Gemini API](https://deepmind.google/technologies/gemini/) by Google
- [FastAPI](https://fastapi.tiangolo.com/)
- [React.js](https://reactjs.org/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

## 📬 Contact
Built with 💙 by [Nick Efe Oni](efeoni10@gmail.com).

Feel free to fork, star, and share your feedback!

## ✍️ Author

**Nick Efe Oni**  
[GitHub](https://github.com/VictoriousWealth) • [LinkedIn](https://www.linkedin.com/in/nick-efe-oni)  
✉️ efeoni10@gmail.com
