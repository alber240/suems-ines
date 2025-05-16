import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import Events from './pages/Events';
import Login from './pages/Login';

function App() {
  return (
    <Router>
      <div className="App">
        <header>
          <h1>Smart University Event Management System</h1>
          <nav>
            <Link to="/">Home</Link>
            <Link to="/events">Events</Link>
            <Link to="/login">Login</Link>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/events" element={<Events />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>

        <footer>
          <p>&copy; 2025 INES-Ruhengeri</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
