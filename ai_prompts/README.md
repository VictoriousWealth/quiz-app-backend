# 🧠 AI Prompt Templates

This folder contains the prompt engineering logic used to guide Gemini AI in generating quiz content from user-uploaded documents.

## 📄 Files

### `gemini_prompts.py`
Contains the key prompt templates and formatting logic for:
- Extracting readable and quiz-relevant text from various file types (PDF, DOCX, TXT)
- Asking Gemini to generate multiple-choice and true/false questions from that content
- Asking Gemini to evaluate user answers and return both the correct option and a brief explanation

## 🧪 Prompt Engineering Strategy

Gemini prompts are:
- Carefully structured to minimize ambiguity
- Tuned for factuality, clarity, and coverage
- Parameterized to support batch generation of 5-question sections per uploaded file

Example:
```python
GEN_QUIZ_PROMPT = """
Given the following content:
"""
{extracted_text}
"""
Generate 5 multiple-choice questions (each with 4 options and 1 correct answer) and 2 true/false questions. Return them in the following format:

[
  {
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "A",
    "explanation": "..."
  },
  ...
]
"""
```

## ⚖️ Responsibilities

Prompt logic in this folder is called by:
- `/upload-db/` route (during file upload, to generate first quiz section)
- `/quizzes/{file_id}/generate-more` (to dynamically generate more quiz sections)
- `/answers/` route (to evaluate submitted user answers)

The actual API call to Gemini is handled in `services/gemini_service.py`, while this folder holds the textual logic passed into those requests.

## 🔧 Future Improvements
- Add few-shot examples to the prompts to improve consistency
- Modularize prompts further to support more question types (e.g., fill-in-the-blank, open ended questions)


---

## 📬 Contact
Built with 💙 by [Nick Efe Oni](mailto:efeoni10@gmail.com).

Feel free to fork, star, and share your feedback!

## ✍️ Author

**Nick Efe Oni**  
[GitHub](https://github.com/VictoriousWealth) • [LinkedIn](https://www.linkedin.com/in/nick-efe-oni)  
✉️ [efeoni10@gmail.com](mailto:efeoni10@gmail.com)
