from io import BytesIO
from fastapi.testclient import TestClient
from main import app
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="This is a real test PDF", ln=True)
pdf.output("tests/sample.pdf")


client = TestClient(app)

def test_file_upload(auth_client):
    with open("tests/sample.pdf", "rb") as real_pdf:
        response = auth_client.post(
            "/upload-db",
            files={"file": ("sample.pdf", real_pdf, "application/pdf")}
        )
    assert response.status_code == 200
    assert "questions" in response.json()

