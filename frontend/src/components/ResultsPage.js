import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, Button, Badge } from 'react-bootstrap';

const ResultsPage = ({ darkMode }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const results = location.state?.results || [];
  const userAnswers = location.state?.userAnswers || {};
  const totalQuestions = results.length;
  const correctAnswers = results.filter(q => q.is_correct).length;
  const scorePercent = (correctAnswers / totalQuestions) * 100;
  let badgeBg = '';
  let badgeText = '';

  if (scorePercent >= 70) {
    badgeBg = 'success';  // green
    badgeText = 'light';
  } else if (scorePercent >= 40) {
    badgeBg = 'warning';  // yellow
    badgeText = 'dark';
  } else {
    badgeBg = 'danger';   // red
    badgeText = 'light';
  }


  if (!results.length) {
    return (
      <div className="text-center mt-5">
        <h4>No results found. Please complete a quiz first.</h4>
        <Button
          variant={darkMode ? 'outline-light' : 'primary'}
          onClick={() => navigate('/upload')}
          className="mt-3"
        >
          Back to Upload
        </Button>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h2 className="mb-4 text-center">Quiz Results</h2>
      <h4 className="text-center mb-4">
        You got{' '}
        <Badge
          bg={badgeBg}
          text={badgeText}
          className="px-3 py-2 fs-5"
        >
          {correctAnswers} / {totalQuestions}
        </Badge>{' '}
        correct 🎯
      </h4>

      {results.map((q) => (
        <Card
          key={q.id}
          className={`mb-3 p-3 border-2 ${darkMode ? 'bg-dark text-light border-light' : 'bg-light text-dark border-dark'}`}
        >
          <Card.Title>
            {q.id}. {q.question}
          </Card.Title>
          <Card.Subtitle className="mb-2">
            <strong>Your Answer:</strong>{' '}
            <Badge bg={q.is_correct ? 'success' : 'danger'}>
              {q.user_answer}
            </Badge>
          </Card.Subtitle>
          <Card.Text>
            <strong>Correct Answer:</strong> {q.correct_answer}
          </Card.Text>
          <Card.Text>
            <strong>Explanation:</strong> {q.explanation}
          </Card.Text>
        </Card>
      ))}

      <div className="text-center">
        <Button
          variant={darkMode ? 'outline-light' : 'success'}
          onClick={() => navigate('/upload')}
        >
          Try Another File
        </Button>
      </div>
    </div>
  );
};

export default ResultsPage;
