import os
import google.generativeai as genai
import json

from dotenv import load_dotenv
load_dotenv()  # Make extra sure .env loads here too (safe duplication)

def generate_quiz_from_text(text: str):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = f"""
                You are an assistant helping students learn. Based on the following content, generate a quiz with 5 multiple-choice questions. Each question should have 4 options.

                Text:
                {text}

                Return the result as a JSON object in the following format:
                {{
                "quiz_id": "some_id",
                "questions": [
                    {{
                    "id": 1,
                    "question": "Question here",
                    "options": ["A", "B", "C", "D"]
                    }},
                    ...
                ]
                }}
            """
    response = model.generate_content(prompt)
    print("GEMINI RAW:", response.text)
    return response.text


# load_dotenv()  # Make extra sure .env loads here too (safe duplication)
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
                    "id": 1,
                    "question": "...",
                    "user_answer": "...",
                    "correct_answer": "...",
                    "is_correct": true,
                    "explanation": "..."
                    }},
                    ...
                ]
                }}

                Quiz:
                {quiz_data}

                User Answers:
                {user_answers}
            """
    
    response = model.generate_content(prompt)
    return json.loads(response.text.strip("```json\n").strip("```"))
