import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import FileUpload from './components/FileUpload';
import QuizPage from './components/QuizPage';
import ResultsPage from './components/ResultsPage';
import HistoryPage from './components/HistoryPage';
import AppNavbar from './components/Navbar';
import Login from './components/Login';
import { jwtDecode } from "jwt-decode";
import Dashboard from './components/Dashboard';
import Register from './components/Register'; // at the top

function isTokenValid() {
  const token = localStorage.getItem("token");
  if (!token) return false;

  try {
    const decoded = jwtDecode(token);
    const now = Date.now() / 1000;
    return decoded.exp > now;
  } catch {
    return false;
  }
}

function PrivateRoute({ children }) {
  return isTokenValid() ? children : <Navigate to="/login" />;
}

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <Router>
      <div className={darkMode ? "bg-dark text-light min-vh-100" : "bg-light text-dark min-vh-100"}>
        <AppNavbar darkMode={darkMode} setDarkMode={setDarkMode} />
        <div className="container pt-4">
          <Routes>
            <Route path="/" element={<PrivateRoute><Dashboard darkMode={darkMode} /></PrivateRoute>} />
            <Route path="/quiz" element={<PrivateRoute><QuizPage darkMode={darkMode} /></PrivateRoute>} />
            <Route path="/results" element={<PrivateRoute><ResultsPage darkMode={darkMode} /></PrivateRoute>} />
            <Route path="/history" element={<PrivateRoute><HistoryPage darkMode={darkMode} /></PrivateRoute>} />
            <Route path="/upload" element={<PrivateRoute><FileUpload darkMode={darkMode} /></PrivateRoute>} />
            <Route path="/login" element={
              localStorage.getItem("token") ? <Navigate to="/" /> : <Login darkMode={darkMode} />
            } />
            <Route path="/signup" element={
              localStorage.getItem("token") ? <Navigate to="/" /> : <Register darkMode={darkMode} />
            } />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
