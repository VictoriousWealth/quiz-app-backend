# 🔌 API Design & Endpoints

This document describes the API endpoints between the React frontend and the FastAPI backend.

All protected routes require a valid JWT token in the `Authorization` header:

```bash
Authorization: Bearer <token>
```


---

## 🧾 Authentication

### `POST /auth/register`
- Accepts: `{ email, password, username }`
- Action: Creates a new user account.
- Returns: Success message or error.

### `POST /auth/login`
- Accepts: `{ email, password }`
- Returns: `{ access_token }` on success.

---

## 📤 File Upload & Processing

### `POST /upload-db/`
- Accepts: Multipart file (`.pdf`, `.docx`, `.txt`)
- Action:
  - Extracts text
  - Generates and stores quizzes (1 section = 5 MCQs)
- Returns: Full quiz JSON for the first section.

---

## 🧠 Generate More Quizzes (On-Demand)

### `POST /quizzes/generate/{file_id}`
- Accepts: File ID
- Action: Generates **new** quiz sections (ensures no repetition).
- Returns: Generated quiz section(s).

---

## 📋 Get Dashboard Data

### `GET /dashboard`
- Returns: All uploaded files by the logged-in user.

### `GET /dashboard/files/{file_id}/sections`
- Returns: All quiz sections generated under a specific file.

---

## 📝 Submit Quiz Answers

### `POST /answers/`
- Accepts:
  ```json
  {
    "quizData": { ... },
    "userAnswers": {
      "question_uuid": "selected_option"
    }
  }


- Action:
    - Sends the quiz and answers to Gemini
    - Stores the answers in DB
    - Returns score, correct answers, and explanations

---

## 📊 Results & History

`GET /results/{attempt_id}`
- Returns:
    - Questions, user answers, correct answers, explanations, score
`GET /history`
- Returns:
    - List of latest attempts (1 per quiz section)
    - Each includes file name, section number, and score
`GET /history/{quiz_id}`
- Returns:
    - All attempts for a specific quiz section

---

## 👤 User Info

`GET /me`
    - Returns: `{ id, username, email, created_at }`

---

## 🧪 Testing & Validation Routes

(Not exposed in production – covered in backend `tests/` suite)

---

## ⚙️ Status Codes

- `200 OK`: Successful operation
- `201 Created`: Resource successfully created
- `400 Bad Request`: Malformed data
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Unexpected failure

---

## Related Docs

- [Overview](../docs/architecture/overview.md): High-level description of system components.
- [Data Flow](../docs/architecture/data_flow.md): Describes how data moves from upload to evaluation.
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

