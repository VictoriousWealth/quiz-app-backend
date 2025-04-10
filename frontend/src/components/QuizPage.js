import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Card, Form } from 'react-bootstrap';


const sampleQuiz = {
  quiz_id: "sample123",
  questions: [
    {
      id: 1,
      question: "What is the capital of France?",
      options: ["Paris", "Berlin", "Madrid", "Rome"]
    },
    {
      id: 2,
      question: "Which planet is known as the Red Planet?",
      options: ["Venus", "Mars", "Jupiter", "Saturn"]
    }
  ]
};

const QuizPage = ({ darkMode }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const quiz = location.state?.quizData || sampleQuiz; // ✅ fallback to sample

  const [answers, setAnswers] = useState({});

  const handleChange = (questionId, selectedOption) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: selectedOption
    }));
  };

  const handleSubmit = () => {
    console.log("User answers:", answers);
    // TODO: Send answers to backend and navigate to results page
    navigate('/results', { state: { userAnswers: answers, quizId: quiz.quiz_id } });
  };

  if (!quiz || !quiz.questions) {
    return <p>No quiz data found. Please upload a file first.</p>;
  }

  return (
    <div>
      <h2>Take the Quiz</h2>
      {quiz.questions.map((q, index) => (
        <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : 'bg-light text-dark'}`} key={q.id}>
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
                />
              ))}
            </Form>
          </Card.Body>
        </Card>
      ))}
      <Button variant={darkMode ? 'outline-light' : 'success'} onClick={handleSubmit}>
        Submit Answers
      </Button>
    </div>
  );
};

export default QuizPage;
