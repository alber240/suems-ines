import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Events from './pages/Events';
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';
import './App.css';
import { logout, getUser } from './auth';


function App() {
  return (
    <Router>
      <div className="App">
        {/* HEADER */}
        <header>
          <h1>Smart University Event Management System</h1>
        </header>

        {/* ROUTES */}
        <main>
          <Routes>
            {/* Default Route - Login is the first page */}
            <Route path="/" element={<Login />} />

            {/* Other page routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/events" element={<Events />} />
            <Route path="/home" element={<Home />} />
            <Route path="/admin-dashboard" element={<AdminDashboard />} />

            {/* Catch all - redirect to login if path not matched */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* FOOTER */}
        <footer>
          <p>&copy; 2025 INES-Ruhengeri</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
