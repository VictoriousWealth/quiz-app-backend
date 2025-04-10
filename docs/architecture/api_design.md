# 🔌 API Design & Endpoints

This document outlines the planned API endpoints between the frontend and FastAPI backend.

---

## 📤 File Upload
### `POST /upload`
- Accepts: Multipart file (PDF, DOCX)
- Action: Extracts text and returns a generated quiz
- Returns: Quiz questions (JSON)

---

## 🧠 Quiz Generation (Optional if separated)
### `POST /generate-quiz`
- Accepts: Extracted text (JSON)
- Action: Sends text to Gemini to create quiz
- Returns: Quiz questions (JSON)

---

## 📝 Submit Quiz Answers
### `POST /submit-answers`
- Accepts: Quiz ID, user answers
- Action: Sends answers + original prompt to Gemini
- Returns: Correct answers, explanations, and score

---

## 📚 Fetch Quiz
### `GET /quiz/:id`
- Accepts: Quiz ID
- Returns: Quiz JSON

---

## 📊 View Results
### `GET /results/:quiz_id`
- Accepts: Quiz ID
- Returns: User answers, correct answers, explanations

---

## 🕘 Quiz History
### `GET /quizzes/history`
- Accepts: User ID (or session if anonymous)
- Returns: List of past quizzes and scores


