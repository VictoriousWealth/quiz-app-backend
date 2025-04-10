import React, { useState } from 'react';
import { Button, Form, Card } from 'react-bootstrap';
import API from '../api/api';
import { useNavigate } from 'react-router-dom';


const FileUpload = ({ darkMode }) => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };


  const handleUpload = async () => {
    if (!file) return alert('Please select a file!');
    console.log('Uploading file:', file.name);
  
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const res = await API.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
  
      console.log('Quiz received:', res.data);
      navigate('/quiz', { state: { quizData: res.data } });
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to generate quiz. Please try again.');
    }
  };

  return (
    <Card className={`p-4 ${darkMode ? 'bg-dark text-light' : 'bg-light text-dark'}`}>
      <h2 className="mb-4">Upload a File to Generate Quiz</h2>
      <Form>
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Select a PDF or DOCX file:</Form.Label>
          <Form.Control
            type="file"
            onChange={handleFileChange}
            className={darkMode ? 'bg-secondary text-light' : ''}
          />
        </Form.Group>
        <Button
          variant={darkMode ? 'outline-light' : 'primary'}
          onClick={handleUpload}
        >
          Upload & Generate Quiz
        </Button>
      </Form>
    </Card>
  );
};

export default FileUpload;
