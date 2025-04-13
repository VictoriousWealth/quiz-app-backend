# 🧱 System Design Overview

## 🎯 Goal
Build a full-stack AI-powered quiz web application that allows users to upload learning materials (PDF, DOCX, TXT), generate quizzes from the content using Gemini AI, take the quizzes, receive AI-evaluated feedback, and track their progress over time.

## 🗂️ Architecture Style
This is a **classic client-server architecture**, with a React frontend interacting with a FastAPI backend via RESTful API calls. User authentication is handled using **JWT tokens** with optional support for **OAuth2**.

## 🔧 Core Components

### 1. Frontend (React.js + Bootstrap)
- Responsive, accessible UI with support for **dark/light mode**
- Upload interface for learning files
- Quiz interface with answer tracking
- Results page with explanations
- Dashboard and history tracking

### 2. Backend (FastAPI)
- Exposes RESTful API endpoints to the frontend
- Handles file upload and text parsing
- Generates quizzes via Gemini API
- Stores and evaluates user responses
- Manages user authentication (JWT)

### 3. AI Integration (Gemini API)
- Generates quiz questions from raw content
- Stores context to evaluate quiz submissions in the same conversation
- Returns correct answers and explanations per question

### 4. Database (PostgreSQL)
- Stores uploaded files, quizzes, user answers, and results
- Enables users to reattempt quizzes and track their history
- Associates quiz content with the original uploaded file

---

## 📌 Key Features (from User Stories)
- Upload a PDF, DOCX, or TXT file
- Generate a quiz per file and section
- Take quizzes and submit answers
- See correct answers and explanations
- Track previous quiz attempts
- Reattempt quizzes anytime
- Light/dark mode toggle

## 🚀 Deployment
- Intended for Heroku (or other cloud platforms such as Render, Vercel, etc.)
- `.env` file used for local development with keys: `DATABASE_URL`, `GEMINI_API_KEY`, `SECRET_KEY`

## ♿ Accessibility
- Fully keyboard-navigable UI
- Responsive on both desktop and mobile
- Contrast-friendly theme with dark/light toggle

