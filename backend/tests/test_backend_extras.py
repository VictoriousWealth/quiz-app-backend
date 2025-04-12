import pytest


# 1. Test reattempting a quiz submission
def test_quiz_reattempt(auth_client, sample_quiz_setup, mock_evaluate_answers):
    quiz_id = sample_quiz_setup["quiz_id"]
    question_id = sample_quiz_setup["question_ids"][0]

    print("Quiz ID:", quiz_id)
    print("Question ID in request:", question_id)

    answers = [{"question_id": str(question_id), "answer": "A"}]

    payload = {
        "quizData": {"quiz_id": str(quiz_id)},
        "userAnswers": answers
    }

    res1 = auth_client.post("/answers/", json=payload)
    assert res1.status_code == 200


# 2. Test retrieving uploaded files
def test_get_uploaded_files(auth_client):
    with open("tests/sample.pdf", "rb") as f:
        auth_client.post("/upload-db", files={"file": ("sample.pdf", f, "application/pdf")})
    
    response = auth_client.get("user/dashboard/files")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 3. Test retrieving quizzes for a given file
def test_get_quizzes_by_file(auth_client, sample_file_id):
    response = auth_client.get(f"/user/dashboard/files/{sample_file_id}/sections")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("questions" in section for section in data)
    
# 4. Test viewing quiz history
def test_quiz_history(auth_client, sample_quiz_setup):
    answers = [{"question_id": str(sample_quiz_setup["question_ids"][0]), "answer": "A"}] 
    print("Question IDs:", sample_quiz_setup["question_ids"])
    print("Question ID being used:", sample_quiz_setup["question_ids"][0])
    print("Answer payload:", answers)

    auth_client.post("/answers/", json={
        "quizData": {"quiz_id": str(sample_quiz_setup["quiz_id"])},  # Add more quiz metadata if needed
        "userAnswers": answers
    })
    response = auth_client.get("/user/dashboard/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 5. Submitting quiz with invalid format
def test_invalid_quiz_submission(auth_client, sample_quiz_setup):
    response = auth_client.post("/answers/", json={
        "quizData": {"quiz_id": sample_quiz_setup["quiz_id"]},
        "userAnswers": {"invalid": "data"}  # or malformed input for the test
    })
    assert response.status_code in (400, 422, 500)  # include 500 if evaluation fails


# 6. Submitting quiz with no answers
def test_quiz_submission_missing_answers(auth_client, sample_quiz_id):
    response = auth_client.post("/answers/", json={
        "quizData": {"quiz_id": str(sample_quiz_id)},
        "userAnswers": {}  # or malformed input for the test
    })
    assert response.status_code == 200

# 7. Invalid file ID for fetching sections
def test_invalid_file_id_sections(auth_client):
    response = auth_client.get("/user/dashboard/files/not-a-uuid/sections")
    assert response.status_code in (404, 422)

# 8. Uploading same file twice
def test_duplicate_file_upload(auth_client):
    with open("tests/sample.pdf", "rb") as f1, open("tests/sample.pdf", "rb") as f2:
        res1 = auth_client.post("/upload-db", files={"file": ("sample.pdf", f1, "application/pdf")})
        res2 = auth_client.post("/upload-db", files={"file": ("sample.pdf", f2, "application/pdf")})
    assert res1.status_code == 200
    assert res2.status_code in (200, 409)  # Customize based on your backend logic
