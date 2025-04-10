import React, { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import API from '../api/api';
import { useNavigate } from 'react-router-dom';


const FileUpload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const navigate = useNavigate();

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
    <div>
      <h2>Upload a File to Generate Quiz</h2>
      <Form>
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Select a PDF or DOCX file:</Form.Label>
          <Form.Control type="file" onChange={handleFileChange} />
        </Form.Group>
        <Button variant="primary" onClick={handleUpload}>
          Upload & Generate Quiz
        </Button>
      </Form>
    </div>
  );
};

export default FileUpload;
