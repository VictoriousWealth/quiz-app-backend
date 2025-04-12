import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Card, Form } from 'react-bootstrap';
import API from '../api/api';
import '../App.css';

const QuizPage = ({ darkMode }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const quiz = location.state?.quizData;
  const [submitting, setSubmitting] = useState(false);
  const [answers, setAnswers] = useState({});

  const handleChange = (questionId, selectedOption) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: selectedOption
    }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);

    try {
      const token = localStorage.getItem("token");

      const res = await API.post("/answers/", {
        quizData: quiz,
        userAnswers: answers
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const evaluation = res.data;

      navigate("/results", {
        state: {
          quizId: quiz.quiz_id,
          userAnswers: answers,
          results: evaluation.results
        }
      });

    } catch (err) {
      console.error("Answer check failed:", err);
      alert("Failed to check answers. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  if (!quiz || !quiz.questions || quiz.questions.length === 0) {
    return (
      <div className="text-center mt-5">
        <h4>No quiz data found</h4>
        <p>Please upload a file or select a section from the dashboard.</p>
        <div className="d-flex justify-content-center gap-3 mt-3">
          <Button
            variant={darkMode ? "outline-light" : "primary"}
            onClick={() => navigate("/")}
          >
            Go to Dashboard
          </Button>
          <Button
            variant={darkMode ? "outline-light" : "secondary"}
            onClick={() => navigate("/")}
          >
            Go to Upload Page
          </Button>
        </div>
      </div>
    );
  }

  return (
    <>
      {submitting && (
        <div className={`global-overlay ${darkMode ? "dark" : "light"}`}>
          <div className="spinner-border" role="status" />
        </div>
      )}

      <div className="container mt-4">
        <h2>{location.state ? "Take the Quiz" : "Sample Quiz"}</h2>
        {quiz.questions.map((q, index) => (
          <Card
            key={q.id}
            className={`mb-3 ${darkMode ? 'bg-dark text-light border-light' : 'bg-light text-dark border-dark'}`}
          >
            <Card.Body>
              <Card.Title>{index + 1}. {q.question}</Card.Title>
              <Form>
                {q.options.map((option, idx) => (
                  <Form.Check
                    key={idx}
                    type="radio"
                    label={option}
                    name={`question-${q.id}`}
                    value={option}
                    checked={answers[q.id] === option}
                    onChange={() => handleChange(q.id, option)}
                    className="mb-2"
                  />
                ))}
              </Form>
            </Card.Body>
          </Card>
        ))}
        <Button
          variant={darkMode ? 'outline-light' : 'success'}
          onClick={handleSubmit}
          disabled={submitting}
        >
          {submitting ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Submitting...
            </>
          ) : (
            'Submit Answers'
          )}
        </Button>
      </div>
    </>
  );
};

export default QuizPage;
