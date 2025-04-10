# 🔄 System Data Flow

This document outlines the sequence of actions and data flow within the app.

---

## 📥 Upload & Generate Quiz Flow

1. **User uploads file (PDF, DOCX)** via frontend.
2. **Frontend** sends file via `POST /upload` to FastAPI backend.
3. **Backend** extracts raw text from file.
4. **Text** is sent to Gemini API with a prompt: “Generate 5 MCQs from this text.”
5. **Gemini API** returns a structured quiz with questions and multiple choices.
6. **Backend** stores the quiz and returns it to frontend.
7. **User** sees the quiz and starts answering questions.

---

## 🧠 Submit Answers & Evaluate Flow

1. **User completes quiz** and submits answers.
2. **Frontend** sends responses to `POST /submit-answers`.
3. **Backend** retrieves original quiz + conversation history.
4. **Backend** sends user answers + quiz context back to Gemini.
5. **Gemini** evaluates and returns:
   - Correct answers
   - Explanation per question
6. **Backend** stores results and sends them to frontend.
7. **User** sees score, correct answers, and explanations.

---

## 💾 Reattempt or Review Flow

1. **Frontend** requests quiz list via `GET /quizzes/history`.
2. **User** selects a past quiz.
3. **Frontend** fetches quiz via `GET /quiz/:id`.
4. User retakes quiz, and the evaluation process repeats as above.


