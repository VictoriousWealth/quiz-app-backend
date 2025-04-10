import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FileUpload from './components/FileUpload';
import QuizPage from './components/QuizPage';
import ResultsPage from './components/ResultsPage';
import HistoryPage from './components/HistoryPage';
import AppNavbar from './components/Navbar';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <Router>
      <div className={darkMode ? "bg-dark text-light min-vh-100" : "bg-light text-dark min-vh-100"}>
        <AppNavbar darkMode={darkMode} setDarkMode={setDarkMode} />
        <div className="container pt-4">
          <Routes>
            <Route path="/" element={<FileUpload darkMode={darkMode} />} />
            <Route path="/quiz" element={<QuizPage darkMode={darkMode} />} />
            <Route path="/results" element={<ResultsPage darkMode={darkMode} />} />
            <Route path="/history" element={<HistoryPage darkMode={darkMode} />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
