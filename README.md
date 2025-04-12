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
44 detailed screenshots have been uploaded to showcase user flow, dark/light mode, quiz results, and dashboard views.
Here are some visual highlights of the app in both light and dark modes:

### 🔐 Login
<table>
  <tr>
    <td><img src="docs/screenshots/login_light_empty.png" alt="Login Light with no details" width="250"/></td>
    <td><img src="docs/screenshots/login_light_filled.png" alt="Login Light with details filled in" width="250"/></td>
    <td><img src="docs/screenshots/login_dark_empty.png" alt="Login Dark with no details" width="250"/></td>
    <td><img src="docs/screenshots/login_dark_filled.png" alt="Login Dark with details filled in" width="250"/></td>
  </tr>
</table>

---

### 📂 Upload File & Generate Quiz
<table>
  <tr>
    <td><img src="docs/screenshots/upload_light_empty.png" alt="Upload Light with no file chosen" width="250"/></td>
    <td><img src="docs/screenshots/upload_light_filled.png" alt="Upload Light with file chosen" width="250"/></td>
    <td><img src="docs/screenshots/upload_dark_empty.png" alt="Upload Dark with no file chosen" width="250"/></td>
    <td><img src="docs/screenshots/upload_dark_filled.png" alt="Upload Dark with file chosen" width="250"/></td>
    <td><img src="docs/screenshots/upload_dark_loading.png" alt="Upload Dark now uploading file" width="250"/></td>
    <td><img src="docs/screenshots/upload_dark_success.png" alt="Upload Dark now generating quiz" width="250"/></td>
  </tr>
</table>

---

### 🧠 Quiz Page
<table>
  <tr>
    <td><img src="docs/screenshots/quiz_light_empty.png" alt="Quiz Light with no quiz data" width="250"/></td>
    <td><img src="docs/screenshots/quiz_light_filled_top.png" alt="Quiz Light with quiz data Top section" width="250"/></td>
    <td><img src="docs/screenshots/quiz_light_filled_bottom.png" alt="Quiz Light with quiz data Bottom section" width="250"/></td>
    <td><img src="docs/screenshots/quiz_dark_empty.png" alt="Quiz Dark with no quiz data" width="250"/></td>
    <td><img src="docs/screenshots/quiz_dark_filled_top.png" alt="Quiz Dark with quiz data Top section" width="250"/></td>
    <td><img src="docs/screenshots/quiz_dark_filled_bottom.png" alt="Quiz Dark with quiz data Bottom section" width="250"/></td>
    <td><img src="docs/screenshots/quiz_dark_filled_loading.png" alt="Quiz Dark with quiz data loading section" width="250"/></td>
  </tr>
</table>

---

### 📊 Results Page
<table>
  <tr>
    <td><img src="docs/screenshots/results_light_empty.png" alt="Results Light with no results data" width="250"/></td>
    <td><img src="docs/screenshots/results_light_filled_top.png" alt="Results Light with results data Top Section" width="250"/></td>
    <td><img src="docs/screenshots/results_light_filled_bottom.png" alt="Results Light with no results data Bottom Section" width="250"/></td>
    <td><img src="docs/screenshots/results_dark_empty.png" alt="Results Dark with no results data" width="250"/></td>
    <td><img src="docs/screenshots/results_dark_filled_top.png" alt="Results Dark with no results data Top Section" width="250"/></td>
    <td><img src="docs/screenshots/results_dark_filled_bottom.png" alt="Results Dark with no results data Bottom Section" width="250"/></td>
  </tr>
</table>

---

### 🗂️ Dashboard & History
<table>
  <tr>
    <td><img src="docs/screenshots/dashboard_light_empty.png" alt="Dashboard Light with no files data" width="250"/></td>
    <td><img src="docs/screenshots/dashboard_light_filled.png" alt="Dashboard Light with files data" width="250"/></td>
    <td><img src="docs/screenshots/dashboard_light_filled_show_section.png" alt="Dashboard Light with files data showing one or more section" width="250"/></td>
    <td><img src="docs/screenshots/dashboard_dark_empty.png" alt="Dashboard Dark with no files data" width="250"/></td>
    <td><img src="docs/screenshots/dashboard_dark_filled.png" alt="Dashboard Dark with files data" width="250"/></td>
    <td><img src="docs/screenshots/dashboard_dark_filled_show_section.png" alt="Dashboard Dark with files data showing one or more section" width="250"/></td>
  </tr>
  <tr>
    <td><img src="docs/screenshots/history_light_filled.png" alt="History Light" width="250"/></td>
    <td><img src="docs/screenshots/history_light_filled_view_attempts.png" alt="History Light show view attempts" width="250"/></td>
    <td><img src="docs/screenshots/history_dark_filled.png" alt="History Dark" width="250"/></td>
    <td><img src="docs/screenshots/history_dark_filled_view_attempts.png" alt="History Dark show view attempts" width="250"/></td>
  </tr>
</table>

---

## 💡 Future Enhancements
- Admin dashboard
- Shareable quiz links
- Custom quiz generation settings
- Gamification elements (badges, leaderboard)
- Frontend testing

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
Built with 💙 by [Nick Efe Oni](mailto:efeoni10@gmail.com).

Feel free to fork, star, and share your feedback!

## ✍️ Author

**Nick Efe Oni**  
[GitHub](https://github.com/VictoriousWealth) • [LinkedIn](https://www.linkedin.com/in/nick-efe-oni)  
✉️ [efeoni10@gmail.com](mailto:efeoni10@gmail.com)
