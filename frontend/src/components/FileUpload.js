import React, { useState } from 'react';
import { Button, Form, Card, Toast, ToastContainer } from 'react-bootstrap';
import API from '../api/api';
import { useNavigate } from 'react-router-dom';
import Loader from './Loader';
import confetti from 'canvas-confetti';
import '../App.css';

const FileUpload = ({ darkMode }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    const allowedExtensions = ['.pdf', '.docx', '.txt'];

    if (selectedFile) {
      const ext = selectedFile.name.split('.').pop().toLowerCase();
      if (!allowedExtensions.includes(`.${ext}`)) {
        alert('Only PDF, DOCX, and TXT files are supported.');
        e.target.value = null;
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert('Please select a file!');
    console.log('Uploading file:', file.name);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const res = await API.post('/upload-db/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`,
        },
      });
      setShowToast(true);

      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
      });
      
      setTimeout(() => {
        confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      }, 400); // to delay it slightly to sync with toast

      setTimeout(() => {
        navigate('/quiz', { state: { quizData: res.data } });
      }, 2000);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to generate quiz. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {loading && (
        <div className={`global-overlay ${darkMode ? "dark" : "light"}`}>
          <div className="spinner-border" role="status" />
        </div>
      )}
  
      <ToastContainer position="bottom-end" className="p-3">
        <Toast
          bg="success"
          show={showToast}
          onClose={() => setShowToast(false)}
          delay={2000}
          autohide
        >
          <Toast.Header>
            <strong className="me-auto">Quiz Ready!</strong>
          </Toast.Header>
          <Toast.Body>Your AI-generated quiz has been created 🎉</Toast.Body>
        </Toast>
      </ToastContainer>
  
      <Card className={`p-4 ${darkMode ? 'bg-dark text-light border-light' : 'bg-light text-dark border-dark'}`}>
        <h2 className="mb-4">Upload a File to Generate Quiz</h2>
        <Form>
          <Form.Group controlId="formFile" className="mb-3">
            <Form.Label>Select a PDF, DOCX, or TXT file:</Form.Label>
            <Form.Control
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              className={`mb-3 ${darkMode ? 'bg-secondary text-light border-light' : 'border-dark'}`}
            />
          </Form.Group>
          <Button
            variant={darkMode ? 'outline-light' : 'primary'}
            onClick={handleUpload}
            disabled={!file}
          >
            Upload & Generate Quiz
          </Button>
        </Form>
      </Card>
    </>
  );
  
};

export default FileUpload;
