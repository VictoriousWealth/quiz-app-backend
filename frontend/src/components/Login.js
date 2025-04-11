import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login({ darkMode }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.access_token); // ✅ correct
      navigate("/"); // Redirect after login
    } else {
      setError("Invalid email or password.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };
  

  return (
    <div className={`card ${darkMode ? "bg-secondary text-light" : "bg-white text-dark"} mx-auto`} style={{ maxWidth: '400px' }}>
      <div className="card-body">
        <h3 className="card-title mb-4">Login</h3>
        {error && <div className="alert alert-danger">{error}</div>}
        <form onSubmit={handleLogin}>
          <div className="mb-3">
            <label>Email</label>
            <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div className="mb-3">
            <label>Password</label>
            <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit" className="btn btn-primary w-100">Log In</button>
        </form>
      </div>
    </div>
  );
}

export default Login;
