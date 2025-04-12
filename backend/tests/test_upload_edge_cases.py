
def test_docx_upload(auth_client):
    with open("tests/sample.docx", "rb") as docx_file:
        response = auth_client.post(
            "/upload-db",
            files={"file": ("sample.docx", docx_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) > 0

def test_empty_pdf_upload(auth_client):
    with open("tests/empty.pdf", "rb") as empty_pdf:
        response = auth_client.post(
            "/upload-db",
            files={"file": ("empty.pdf", empty_pdf, "application/pdf")}
        )
    # You may want to return 422 or 400 depending on how you handle empty content
    assert response.status_code in (400, 422, 500)

def test_disallowed_filetype(auth_client):
    with open("tests/fake.exe", "rb") as exe_file:
        response = auth_client.post(
            "/upload-db",
            files={"file": ("fake.exe", exe_file, "application/octet-stream")}
        )
    assert response.status_code in (400, 422, 415)

def test_reject_dangerous_file_type(client, test_user_token):
    with open("tests/fake.exe", "rb") as f:
        response = client.post(
            "/upload-db",
            files={"file": ("fake.exe", f, "application/x-msdownload")},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
    assert response.status_code in (400, 415)
    assert "error" in response.json()

def test_malformed_file_upload(client, test_user_token):
    with open("tests/malformed.docx", "rb") as f:
        response = client.post(
            "/upload-db",
            files={"file": ("malformed.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
    assert response.status_code in (400, 422, 500)  # depending on how you handle it
