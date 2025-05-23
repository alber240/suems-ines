// ✅ Let's add Edit and Delete functionality to AdminDashboard.js
// This assumes you've already implemented the POST /api/events route.

// We'll add:
// - A button to edit each event
// - A button to delete each event
// - A form that supports both creating and editing

// We'll update the AdminDashboard component to include these features

import React, { useEffect, useState } from 'react';
import './AdminDashboard.css';
import { logout, getUser } from '../auth';
import { useNavigate } from 'react-router-dom';

function AdminDashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [events, setEvents] = useState([]);
  const [editingEventId, setEditingEventId] = useState(null);
  const [formData, setFormData] = useState({
    title: '', description: '', location: '', event_type: 'Workshop',
    date: '', start_time: '', end_time: '', target_roles: '',
    faculty: '', department: '', nationality: ''
  });
  const [message, setMessage] = useState('');

  const navigate = useNavigate();
  const user = getUser();

  const fetchEvents = () => {
    fetch('http://localhost:5000/api/events')
      .then(res => res.json())
      .then(data => setEvents(data));
  };

  useEffect(() => {
    fetchEvents();
    fetch('http://localhost:5000/api/dashboard')
      .then(res => res.json())
      .then(data => setDashboardData(data));
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const url = editingEventId
      ? `http://localhost:5000/api/events/${editingEventId}`
      : 'http://localhost:5000/api/events';
    const method = editingEventId ? 'PUT' : 'POST';

    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
      .then(res => res.json())
      .then(data => {
        setMessage(data.message || 'Success');
        setFormData({ title: '', description: '', location: '', event_type: 'Workshop', date: '', start_time: '', end_time: '', target_roles: '', faculty: '', department: '', nationality: '' });
        setEditingEventId(null);
        fetchEvents();
      });
  };

  const handleEdit = (event) => {
    setEditingEventId(event.event_id);
    setFormData({
      title: event.title,
      description: event.description || '',
      location: event.location,
      event_type: event.event_type || 'Other',
      date: event.date,
      start_time: event.start_time || '',
      end_time: event.end_time || '',
      target_roles: event.target_roles || '',
      faculty: event.faculty || '',
      department: event.department || '',
      nationality: event.nationality || ''
    });
  };

  const handleDelete = (id) => {
    if (!window.confirm('Are you sure you want to delete this event?')) return;
    fetch(`http://localhost:5000/api/events/${id}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(() => fetchEvents());
  };

  return (
    <div className="admin-dashboard">
      <header className="admin-header">
        <h2>🎓 SUEMS Admin Dashboard</h2>
        <div>
          <p>Welcome, <strong>{user?.name}</strong> ({user?.role})</p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <section className="admin-section">
        <h3>{editingEventId ? '✏️ Edit Event' : '➕ Create Event'}</h3>
        {message && <p>{message}</p>}
        <form onSubmit={handleSubmit} className="event-form">
          <input type="text" name="title" value={formData.title} placeholder="Title" onChange={handleInputChange} required />
          <textarea name="description" value={formData.description} placeholder="Description" onChange={handleInputChange} />
          <input type="text" name="location" value={formData.location} placeholder="Location" onChange={handleInputChange} />
          <input type="date" name="date" value={formData.date} onChange={handleInputChange} />
          <input type="time" name="start_time" value={formData.start_time} onChange={handleInputChange} />
          <input type="time" name="end_time" value={formData.end_time} onChange={handleInputChange} />
          <select name="event_type" value={formData.event_type} onChange={handleInputChange}>
            <option>Workshop</option><option>Seminar</option><option>Sports</option><option>Fair</option><option>Ceremony</option><option>Other</option>
          </select>
          <select name="target_roles" value={formData.target_roles} onChange={handleInputChange}>
            <option value="">Eligible Role</option>
            <option value="Student">Student</option>
            <option value="Staff">Staff</option>
            <option value="Administrator">Administrator</option>
          </select>
          <input type="text" name="faculty" value={formData.faculty} placeholder="Faculty" onChange={handleInputChange} />
          <input type="text" name="department" value={formData.department} placeholder="Department" onChange={handleInputChange} />
          <select name="nationality" value={formData.nationality} onChange={handleInputChange}>
            <option value="">Nationality</option>
            <option value="Local">Local</option>
            <option value="International">International</option>
          </select>
          <button type="submit">{editingEventId ? 'Update' : 'Create'} Event</button>
        </form>
      </section>

      <section className="admin-section">
        <h3>📋 Existing Events</h3>
        <ul>
          {events.map(evt => (
            <li key={evt.event_id}>
              <strong>{evt.title}</strong> ({evt.date}) — {evt.location} <br/>
              <button onClick={() => handleEdit(evt)}>Edit</button>
              <button onClick={() => handleDelete(evt.event_id)}>Delete</button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default AdminDashboard;
