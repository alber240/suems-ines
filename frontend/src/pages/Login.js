import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { saveUser } from '../auth'; // Save user info to localStorage
import './Login.css';

function Login() {
  const [form, setForm] = useState({
    email: '',
    password: ''
  });

  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = (e) => {
    e.preventDefault();

    // ✅ Just save basic user and redirect to home
    if (form.email && form.password) {
      saveUser({
        email: form.email,
        name: form.email.split('@')[0] || 'User'
      });

      navigate('/home'); // or navigate('/events')
    } else {
      setError('Please fill in both email and password.');
    }
  };

  return (
    <div className="login-container">
      <h2>🎓 Smart University Event Management System</h2>

      <form onSubmit={handleLogin} className="login-form">
        <input
          type="email"
          name="email"
          placeholder="Email address"
          value={form.email}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <button type="submit">Login</button>
        {error && <p className="error-msg">{error}</p>}
      </form>
    </div>
  );
}

export default Login;
