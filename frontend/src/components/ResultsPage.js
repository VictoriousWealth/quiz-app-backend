import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, Button, Badge } from 'react-bootstrap';

const sampleEvaluated = {
  1: {
    correct: "Paris",
    explanation: "Paris is the capital of France."
  },
  2: {
    correct: "Mars",
    explanation: "Mars is known as the Red Planet."
  }
};

const ResultsPage = ({ darkMode }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const userAnswers = location.state?.userAnswers || {};
  const quizId = location.state?.quizId || "sample123";
  const evaluated = location.state?.evaluated || sampleEvaluated;

  const questions = [
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
  ];

  return (
    <div>
      <h2>Quiz Results</h2>
      <p>Quiz ID: {quizId}</p>
      {questions.map((q, index) => {
        const userAnswer = userAnswers[q.id];
        const correctAnswer = evaluated[q.id]?.correct;
        const explanation = evaluated[q.id]?.explanation;
        const isCorrect = userAnswer === correctAnswer;

        return (
          <Card className={`mb-3 ${darkMode ? 'bg-dark text-light' : 'bg-light text-dark'}`} key={q.id} >
            <Card.Body>
              <Card.Title>{index + 1}. {q.question}</Card.Title>
              <p>
                Your Answer:{" "}
                <Badge bg={isCorrect ? "success" : "danger"}>
                  {userAnswer || "No Answer"}
                </Badge>
              </p>
              <p>
                Correct Answer:{" "}
                <Badge bg="info">{correctAnswer}</Badge>
              </p>
              <p><strong>Explanation:</strong> {explanation}</p>
            </Card.Body>
          </Card>
        );
      })}
      <Button variant={darkMode ? 'outline-light' : 'primary'} onClick={() => navigate('/')}>
        Try Another Quiz
      </Button>
    </div>
  );
};

export default ResultsPage;
