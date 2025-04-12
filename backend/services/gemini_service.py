import os
import uuid
import json
import re
import google.generativeai as genai

from dotenv import load_dotenv
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models import Quiz, Question

load_dotenv()


# === Utility to generate unique UUIDs ===
def generate_unique_uuid(session, model, column):
    while True:
        new_id = str(uuid.uuid4())
        result = session.execute(select(model).where(column == new_id))
        if not result.scalars().first():
            return new_id



# === Helper to safely extract JSON from Gemini ===
def extract_json(response_text: str):
    try:
        json_text = re.search(r'\{.*\}', response_text, re.DOTALL).group(0)
        return json.loads(json_text)
    except Exception as e:
        print("RAW Gemini response:\n", response_text)
        raise ValueError(f"Failed to parse Gemini response as JSON: {e}")


# === Gemini quiz generator with UUID injection ===
async def generate_quiz_from_text(text: str, db: Session):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    prompt = f"""
You are an assistant helping students learn. Based on the following content, generate a quiz with 5 multiple-choice questions. Each question must have 4 options and exactly one correct answer.

Text:
{text}

Return JSON in the following format:
{{
  "questions": [
    {{
      "question": "Question here",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "Explanation here"
    }}
  ]
}}
    """

    response = model.generate_content(prompt)
    print("GEMINI RAW:", response.text)
    data = extract_json(response.text)

    for q in data["questions"]:
        q["id"] = generate_unique_uuid(db, Question, Question.id)

    return data["questions"]


# === Evaluate answers using Gemini ===
def evaluate_answers(quiz_data, user_answers):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    prompt = f"""
You are an AI tutor.

Below is a quiz and a user's selected answers. For each question, return:
- the correct answer
- whether the user was right
- a brief explanation

Respond strictly in JSON format as:

{{
  "results": [
    {{
      "id": "uuid",
      "question": "...",
      "user_answer": "...",
      "correct_answer": "...",
      "is_correct": true,
      "explanation": "..."
    }}
  ]
}}

Quiz:
{quiz_data}

User Answers:
{user_answers}
    """

    response = model.generate_content(prompt)
    return extract_json(response.text)


# === Additional quiz generator (no duplicates) ===
async def generate_additional_questions(text, existing_questions, db: Session):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    prompt = f"""
You are a quiz-generating assistant.

Based on the text below, generate new multiple-choice questions (4 options and 1 correct answer) that are *not* duplicates of these:

{json.dumps(existing_questions)}

Text:
{text}

Return JSON in the format:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "..."
    }}
  ]
}}
    """

    response = model.generate_content(prompt)
    print("GEMINI RAW:", response.text)
    data = extract_json(response.text)

    for q in data["questions"]:
        q["id"] = generate_unique_uuid(db, Question, Question.id)

    return data["questions"]
