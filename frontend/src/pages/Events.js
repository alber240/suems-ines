import React, { useEffect, useState } from 'react';
import './Events.css'; // Styling for events page

function Events() {
  // State to hold list of all events fetched from the backend
  const [events, setEvents] = useState([]);

  // Holds the currently selected event for registration
  const [selectedEvent, setSelectedEvent] = useState(null);

  // Form data for registration
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    faculty: '',
    department: '',
    role: '',
    reg_id: ''
  });

  // Form and feedback states
  const [submitted, setSubmitted] = useState(false);   // whether user has submitted the form
  const [message, setMessage] = useState('');          // success message
  const [error, setError] = useState('');              // error message
  const [loading, setLoading] = useState(false);       // loading indicator for form submission

  // Fetch all events on component mount
  useEffect(() => {
    fetch('http://localhost:5000/api/events')
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(err => console.error('Error loading events:', err));
  }, []);

  // Called when user clicks "Register" button
  const openModal = (event) => {
    setSelectedEvent(event); // set current event
    setFormData({            // reset form fields
      name: '',
      email: '',
      phone: '',
      faculty: '',
      department: '',
      role: '',
      reg_id: ''
    });
    setSubmitted(false);
    setMessage('');
    setError('');
  };

  // Close the modal
  const closeModal = () => {
    setSelectedEvent(null);
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true); // show spinner

    // Prepare payload for backend
    const payload = {
      name: formData.name,
      email: formData.email,
      phone: formData.phone,
      faculty: formData.faculty,
      department: formData.department,
      role: formData.role,
      registration_no: formData.reg_id,
      event_id: selectedEvent.event_id
    };

    // Debug log to console
    console.log('✅ Registered payload:', payload);

    // Send to backend
    fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => {
        if (res.status === 201) return res.json(); // success response
        return res.json().then(err => Promise.reject(err)); // error response
      })
      .then(data => {
        setMessage(data.message || '✅ Successfully registered!');
        setError('');
        setSubmitted(true); // hide form
        setTimeout(() => {
          setSubmitted(false);
          setMessage('');
          closeModal();
        }, 2000);
      })
      .catch(error => {
        setError(error.error || '❌ Registration failed.');
        setMessage('');
      })
      .finally(() => {
        setLoading(false); // hide spinner
      });
  };

  return (
    <div className="events-page" style={{ padding: '20px' }}>
      <h2>📅 All University Events</h2>

      {/* Loop through all events and show a card */}
      {events.map(event => (
        <div key={event.event_id} className="event-card">
          <h3>{event.title}</h3>
          <p><strong>Date:</strong> {event.date || 'TBD'}</p>
          <p><strong>Eligible:</strong> {Array.isArray(event.target_roles) ? event.target_roles.join(', ') : 'All'}</p>
          <button onClick={() => openModal(event)}>Register</button>
        </div>
      ))}

      {/* Modal: Shown when user clicks Register */}
      {selectedEvent && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Register for: {selectedEvent.title}</h3>

            {/* Feedback messages */}
            {message && <p className="success-message">{message}</p>}
            {error && <p className="error-message">{error}</p>}

            {/* Form */}
            {!submitted && (
              <form onSubmit={handleSubmit}>
                <input
                  type="text"
                  placeholder="Full Name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />

                <input
                  type="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />

                <input
                  type="text"
                  placeholder="Phone Number"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  required
                />

                <select
                  value={formData.faculty}
                  onChange={(e) => setFormData({ ...formData, faculty: e.target.value })}
                  required
                >
                  <option value="">Select Faculty</option>
                  <option value="Faculty of Science">Faculty of Science</option>
                  <option value="Faculty of Education">Faculty of Education</option>
                  <option value="Faculty of Law">Faculty of Law</option>
                  <option value="Other">Other</option>
                </select>

                <input
                  type="text"
                  placeholder="Department"
                  value={formData.department}
                  onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                  required
                />

                <select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  required
                >
                  <option value="">Select Role</option>
                  <option value="Student">Student</option>
                  <option value="Staff">Staff</option>
                  <option value="Administrator">Administrator</option>
                </select>

                <input
                  type="text"
                  placeholder="Registration No / ID No"
                  value={formData.reg_id}
                  onChange={(e) => setFormData({ ...formData, reg_id: e.target.value })}
                  required
                />

                <button type="submit">Submit Registration</button>

                {/* Spinner while submitting */}
                {loading && <p style={{ color: 'blue' }}>⏳ Submitting...</p>}
              </form>
            )}

            {/* Close modal button */}
            <button className="close-btn" onClick={closeModal}>X</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Events;
