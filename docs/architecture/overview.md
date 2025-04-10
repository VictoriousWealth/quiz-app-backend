# 🧱 System Design Overview

## 🎯 Goal
Build a web app that allows a user to upload a file and generate quiz questions using Gemini AI. The user then answers the quiz, and the app provides correct answers and explanations by sending the answers back to Gemini in the same conversation.

## 🔧 Core Components

### 1. Frontend (React.js + Bootstrap)
- File upload interface
- Quiz-taking UI
- Results display

### 2. Backend (FastAPI)
- File handling & text extraction
- API endpoints to interact with frontend
- Integration with Gemini API
- Quiz & result management

### 3. AI Integration (Gemini API)
- Generates quiz questions from file content
- Evaluates user answers using prompt + earlier conversation
- Provides explanations per question

### 4. Database (PostgreSQL or MongoDB)
- Stores quizzes, answers, results
- Enables reattempts and progress tracking

---

## 📌 Key Features (from User Stories)
- Upload files (PDF, DOCX, etc.)
- Generate quiz questions
- Take quizzes directly in the app
- Submit answers and get explanations
- Save and review past quizzes
- Reattempt previous quizzes
