// src/components/HistoryPage.js
import React, { useEffect, useState } from 'react';
import API from '../api/api';
import { Table, Card, Button, Modal } from 'react-bootstrap';

const HistoryPage = ({ darkMode }) => {
  const [history, setHistory] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [attempts, setAttempts] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState(null);

  useEffect(() => {
    API.get('/user/dashboard/history', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      }
    })
    .then(res => setHistory(res.data))
    .catch(err => console.error("Failed to load history", err));
  }, []);

  const handleViewAttempts = async (quizId) => {
    try {
      const res = await API.get(`/user/dashboard/quiz/${quizId}/attempts`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        }
      });
      setSelectedQuizId(quizId);
      setAttempts(res.data);
      setShowModal(true);
    } catch (err) {
      console.error("Failed to fetch attempts", err);
      alert("Could not fetch attempts. Try again later.");
    }
  };

  return (
    <div className="mt-4">
      <h2 className="mb-4">Quiz History</h2>
      {history.length === 0 ? (
        <Card className={`p-3 ${darkMode ? "bg-dark text-light" : "bg-light text-dark"}`}>
          <p className="mb-0">No quiz attempts yet.</p>
        </Card>
      ) : (
        <Table striped bordered hover responsive variant={darkMode ? 'dark' : 'light'}>
          <thead>
            <tr>
              <th>Filename - Section</th>
              <th>Score</th>
              <th>Submitted At</th>
              <th>Attempts</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item, index) => (
              <tr key={index}>
                <td>{item.label}</td>
                <td>{item.score} / {item.num_questions}</td>
                <td>{new Date(item.submitted_at).toLocaleString()}</td>
                <td>
                  <Button
                    variant={darkMode ? 'outline-light' : 'outline-primary'}
                    size="sm"
                    onClick={() => handleViewAttempts(item.quiz_id)}
                  >
                    View All Attempts
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      <Modal
        show={showModal}
        onHide={() => setShowModal(false)}
        centered
        size="lg"
        className={darkMode ? "dark-modal" : ""}
      >
        <Modal.Header closeButton className={darkMode ? "bg-dark text-light" : ""}>
          <Modal.Title>Attempts for Quiz</Modal.Title>
        </Modal.Header>
        <Modal.Body className={darkMode ? "bg-dark text-light" : ""}>
          {attempts.length === 0 ? (
            <p>No attempts found.</p>
          ) : (
            <Table striped bordered hover variant={darkMode ? "dark" : "light"}>
              <thead>
                <tr>
                  <th>Filename - Section</th>
                  <th>Score</th>
                  <th>Submitted At</th>
                </tr>
              </thead>
              <tbody>
                {attempts.map((attempt, i) => (
                  <tr key={i}>
                    <td>{attempt.label}</td>
                    <td>{attempt.score} / {attempt.num_questions}</td>
                    <td>{new Date(attempt.submitted_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Modal.Body>
        <Modal.Footer className={darkMode ? "bg-dark text-light" : ""}>
          <Button variant={darkMode ? "outline-light" : "secondary"} onClick={() => setShowModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default HistoryPage;
