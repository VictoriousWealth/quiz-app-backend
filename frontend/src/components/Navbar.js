import React from 'react';
import { Navbar, Nav, Container, Form } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const AppNavbar = ({ darkMode, setDarkMode }) => {
  return (
    <Navbar bg={darkMode ? "dark" : "light"} variant={darkMode ? "dark" : "light"} expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">QuizGen</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Upload</Nav.Link>
            <Nav.Link as={Link} to="/quiz">Quiz</Nav.Link>
            <Nav.Link as={Link} to="/results">Results</Nav.Link>
            <Nav.Link as={Link} to="/history">History</Nav.Link>
          </Nav>
          <Form.Switch
            id="darkModeSwitch"
            checked={darkMode}
            onChange={() => setDarkMode(!darkMode)}
            label="🌙"
            className="text-nowrap"
          />
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
