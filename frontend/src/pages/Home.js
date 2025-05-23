import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const [events, setEvents] = useState([]);
  const [filteredEvents, setFilteredEvents] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [question, setQuestion] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/api/events')
      .then(res => res.json())
      .then(data => {
        setEvents(data);
        setFilteredEvents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching events:', err);
        setLoading(false);
      });
  }, []);

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    const results = events.filter(event =>
      event.title.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredEvents(results);
  };

  const handleQuestionSubmit = () => {
    if (question.trim() !== '') {
      setSubmitted(true);
      setTimeout(() => setSubmitted(false), 3000); // reset after 3s
      setQuestion('');
    }
  };

  return (
    <div className="home-container" style={{ padding: '20px' }}>
      <h1>🎓 Welcome to SUEMS</h1>
      <p>The Smart University Event Management System helps INES-Ruhengeri plan, manage, and track university events.</p>

      <h2 style={{ marginTop: '30px' }}>📅 Upcoming Events</h2>

      {/* Search Input */}
      <input
        type="text"
        value={searchQuery}
        onChange={handleSearch}
        placeholder="Search events by title..."
        style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
      />

      {/* Loading or Events */}
      {loading ? (
        <p>Loading events...</p>
      ) : filteredEvents.length > 0 ? (
        filteredEvents.map(event => (
          <div key={event.event_id} style={{
            border: '1px solid #ccc',
            borderRadius: '8px',
            padding: '15px',
            marginBottom: '10px',
            backgroundColor: '#f9f9f9'
          }}>
            <h3>{event.title}</h3>
            <p><strong>Date:</strong> {event.date || 'TBD'}</p>
            <p><strong>Eligible:</strong> {Array.isArray(event.target_roles) ? event.target_roles.join(', ') : 'Everyone'}</p>
          </div>
        ))
      ) : (
        <p>No events found.</p>
      )}

      {/* Quick Navigation */}
      <h2 style={{ marginTop: '40px' }}>🔗 Quick Links</h2>
      <ul>
        <li><Link to="/events">📄 View All Events</Link></li>
        <li><Link to="/login">🔐 Login</Link></li>
        <li><Link to="/admin-dashboard">📊 Admin Dashboard</Link></li>
      </ul>

      {/* Ask a Question */}
      <h2 style={{ marginTop: '40px' }}>❓ Ask a Question</h2>
      <input
        type="text"
        value={question}
        onChange={e => setQuestion(e.target.value)}
        placeholder="Type your question here..."
        style={{ width: '80%', padding: '8px' }}
      />
      <br />
      <button onClick={handleQuestionSubmit} style={{ marginTop: '10px', padding: '8px 16px' }}>Send</button>

      {submitted && (
        <p style={{ color: 'green', marginTop: '10px' }}>✅ Thank you! We’ll respond to your question soon.</p>
      )}

      <footer style={{ marginTop: '40px', color: '#555' }}>
        <hr />
        <p>&copy; 2025 INES-Ruhengeri | Smart University Event Management System</p>
      </footer>
    </div>
  );
}

export default Home;
