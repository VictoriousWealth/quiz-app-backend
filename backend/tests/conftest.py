import sys
import os
import json
import uuid
import pytest

from fastapi.testclient import TestClient
from unittest.mock import patch
from jose import jwt

# Ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from db.session import SessionLocal
from db.models import User, UploadedFile, Quiz, Question
from auth.utils import SECRET_KEY, ALGORITHM

# ✅ Create test files
from docx import Document
from fpdf import FPDF
from unittest.mock import patch
import pytest

os.makedirs("tests", exist_ok=True)

doc = Document()
doc.add_paragraph("This is a test docx file with quiz content.")
doc.save("tests/sample.docx")

pdf = FPDF()
pdf.add_page()
pdf.output("tests/empty.pdf")

with open("tests/fake.exe", "wb") as f:
    f.write(b"This is not an executable.")

with open("tests/malformed.docx", "wb") as f:
    f.write(b"This is not a real DOCX file.\x00\x01\x02\xff\xfe")

with open("tests/sample.txt", "w", encoding="utf-8") as f:
    f.write("This is a plain text file.")

with open("tests/bad.json", "w", encoding="utf-8") as f:
    f.write('{"quiz": [ {"question": "What is FastAPI?" "options": ["Framework", "IDE", "Language"]} ]')

print("✅ All test files created.")

# ============================== FIXTURES ==============================

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user_token(client):
    test_email = f"testuser+{uuid.uuid4().hex[:6]}@example.com"
    password = "strongpass123"

    signup_resp = client.post("/auth/signup", json={
        "email": test_email,
        "password": password,
        "full_name": "Test User"
    })
    print("SIGNUP RESPONSE:", signup_resp.status_code, signup_resp.json())

    response = client.post(
        "/auth/login",
        data={"username": test_email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print("LOGIN RESPONSE:", response.status_code, response.json())

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_client(client, test_user_token):
    client.headers.update({
        "Authorization": f"Bearer {test_user_token}"
    })

    # Attach decoded user_id to auth_client for reuse
    payload = jwt.decode(test_user_token, SECRET_KEY, algorithms=[ALGORITHM])
    client.user_id = payload["sub"]

    return client


@pytest.fixture(autouse=True)
def mock_gemini(sample_quiz_setup):
    quiz_id = sample_quiz_setup["quiz_id"]
    question_ids = sample_quiz_setup["question_ids"]

    with patch("services.gemini_service.evaluate_answers") as mock:
        mock.return_value = {
            "results": [
                {
                    "id": question_ids[0],
                    "user_answer": "A",
                    "is_correct": True
                }
            ]
        }
        yield mock



@pytest.fixture
def sample_file_id(auth_client):
    db = SessionLocal()
    file = UploadedFile(
        id=str(uuid.uuid4()),
        user_id=auth_client.user_id,
        filename="sample123.pdf",
        original_name="test_upload.pdf",
        file_type="pdf"
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    db.close()
    return file.id


@pytest.fixture
def sample_quiz_id(sample_file_id):
    db = SessionLocal()
    quiz = Quiz(id=str(uuid.uuid4()), file_id=sample_file_id)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    questions = [
        Question(
            id=str(uuid.uuid4()),
            quiz_id=quiz.id,
            text=f"Question {i}",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Because A is correct."
        ) for i in range(1, 6)
    ]
    db.add_all(questions)
    db.commit()
    quiz_id = quiz.id 
    db.close()
    return quiz_id


@pytest.fixture
def sample_quiz_setup(auth_client):
    db = SessionLocal()

    file_id = uuid.uuid4()
    quiz_id = uuid.uuid4()

    file = UploadedFile(
        id=file_id,
        user_id=auth_client.user_id,
        filename="sample.pdf",
        original_name="sample.pdf",
        file_type="pdf"
    )
    db.add(file)

    quiz = Quiz(id=quiz_id, file_id=file_id)
    db.add(quiz)

    questions = []
    question_ids = []

    for i in range(1, 6):
        q_id = str(uuid.uuid4())
        q = Question(
            id=q_id,
            quiz_id=quiz_id,
            text=f"Sample Question {i}",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Because A is correct."
        )
        questions.append(q)
        question_ids.append(q_id)

    db.add_all(questions)
    db.commit()

    db.close()

    return {
        "quiz_id": str(quiz_id),
        "file_id": str(file_id),
        "question_ids": question_ids,
        "user_id": auth_client.user_id
    }

@pytest.fixture
def mock_evaluate_answers(sample_quiz_setup):
    question_id = sample_quiz_setup["question_ids"][0]
    print("Sent question ID:", question_id)

    mock_response = {
        "results": [
            {
                "id": str(question_id),  # ✅ Must match seeded UUID
                "question": "Sample Question?",
                "user_answer": "A",
                "correct_answer": "A",
                "is_correct": True,
                "explanation": "Because A is correct."
            }
        ]
    }
    print("Mocked Gemini response ID:", mock_response["results"][0]["id"])


    with patch("routes.answers.evaluate_answers", return_value=mock_response):
        yield
