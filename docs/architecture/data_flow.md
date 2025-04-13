# 🔄 System Data Flow

This document outlines the updated data flow in the AI-Powered Quiz Web App.

---

## 📥 Upload & Auto-Generate Quiz Flow

1. **User uploads a file** (`.pdf`, `.docx`, or `.txt`) via the React frontend.
2. **Frontend** sends file via `POST /upload-db/` to the FastAPI backend.
3. **Backend**:
   - Extracts raw text from the file.
   - Sends prompt and text to Gemini API.
   - Generates **initial quiz section** (5 MCQs).
   - Stores file and generated quizzes.
4. **Gemini API** returns formatted multiple-choice questions.
5. **Backend** returns the quiz to the frontend.
6. **User** sees the quiz and begins answering.

---

## ➕ Generate Additional Quiz Sections

1. **User clicks "Generate More Quizzes"** on a file from the dashboard.
2. **Frontend** sends request to `POST /quizzes/generate/{file_id}`.
3. **Backend**:
   - Retrieves file text.
   - Tracks previously generated questions.
   - Sends request to Gemini API to create **non-redundant** sections.
   - Stores newly generated quiz section(s).
4. Returns fresh quiz section to the frontend.

---

## 🧠 Submit Answers & Evaluation Flow

1. **User answers a quiz section** and clicks Submit.
2. **Frontend** sends `POST /answers/` with:
   - `quizData` (the full quiz section object)
   - `userAnswers` (dictionary of `question_id: selected_option`)
3. **Backend**:
   - Sends both the quiz and answers to Gemini API using the same conversation.
   - Receives:
     - Correct answers
     - Explanations
     - Score
   - Stores answers and evaluation in DB.
4. **Frontend** redirects to `/results` with evaluation.
5. **User** sees results, explanations, and score breakdown.

---

## 📊 View Results or Reattempt Flow

1. **Frontend** requests quiz history via `GET /history`.
2. **User** clicks a specific quiz to view attempts.
3. **Frontend** sends `GET /history/{quiz_id}`.
4. **Backend** returns all attempts under that quiz section.
5. User reviews scores or reattempts quiz.

---

## ⚙️ Supporting Services
- **JWT Auth**: Every action is scoped to authenticated users.
- **PostgreSQL**: Stores quizzes, answers, attempts, and files.
- **Gemini API**: Central to quiz generation and evaluation.

---

## Related Docs

- [Overview](../docs/architecture/overview.md): High-level description of system components.
- [API Design](../docs/architecture/api_design.md): RESTful endpoints powering the system.
- [General System Diagram (PDF)](../docs/diagrams/general_system_flow.pdf): Visual architecture representation.
- [System Architecture](../docs/README_architecture.md): Direct access to all technical documentation related to the system design, architecture, and data flow of the **AI-Powered Quiz Web App**.
- [User Stories](../docs/user_stories/20250409_143339_user_story.txt): Features from a user perspective.
- [Backend](../backend/README.md): The Great Backend.
- [Frontend](../frontend/README.md): The Great Frontend.
- [AI Prompts](../ai_prompts/README.md): A deeper dip into AI
- [General README](../README.md): Lost? Teleport back to the start position. 

---

## 📬 Contact
Built with 💙 by [Nick Efe Oni](mailto:efeoni10@gmail.com).

Feel free to fork, star, and share your feedback!

## ✍️ Author

**Nick Efe Oni**  
[GitHub](https://github.com/VictoriousWealth) • [LinkedIn](https://www.linkedin.com/in/nick-efe-oni)  
✉️ [efeoni10@gmail.com](mailto:efeoni10@gmail.com)

---

