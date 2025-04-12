def test_quiz_generation(auth_client, test_user_token):
    # First upload a real file to get a valid file_id
    with open("tests/sample.pdf", "rb") as real_pdf:
        upload_resp = auth_client.post(
            "/upload-db/",  # make sure this matches your real router
            files={"file": ("sample.pdf", real_pdf, "application/pdf")},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert upload_resp.status_code == 200
        file_id = upload_resp.json().get("file_id")

    # Now try generating additional questions
    response = auth_client.post(
        f"/user/dashboard/files/{file_id}/generate",  # ← match the working route
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200
    assert "questions" in response.json()
