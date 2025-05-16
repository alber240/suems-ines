import sqlite3

# Connect or create the database file
conn = sqlite3.connect("suems.db")
cursor = conn.cursor()

# Enable foreign key constraint
cursor.execute("PRAGMA foreign_keys = ON")

# Drop tables if they already exist (for development only)
cursor.execute("DROP TABLE IF EXISTS feedback")
cursor.execute("DROP TABLE IF EXISTS notifications")
cursor.execute("DROP TABLE IF EXISTS registrations")
cursor.execute("DROP TABLE IF EXISTS events")
cursor.execute("DROP TABLE IF EXISTS users")

# Create USERS table
cursor.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('Student', 'Admin', 'Staff')) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);
""")

# Create EVENTS table
cursor.execute("""
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    event_type TEXT CHECK(event_type IN ('Workshop', 'Seminar', 'Sports', 'Fair', 'Ceremony', 'Other')),
    date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);
""")

# Create REGISTRATIONS table
cursor.execute("""
CREATE TABLE registrations (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('Registered', 'Cancelled', 'Attended', 'Missed')) DEFAULT 'Registered',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);
""")

# Create NOTIFICATIONS table
cursor.execute("""
CREATE TABLE notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    method TEXT CHECK(method IN ('SMS', 'Email', 'Both')) NOT NULL,
    delivery_status TEXT CHECK(delivery_status IN ('Sent', 'Failed', 'Pending')) DEFAULT 'Pending',
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);
""")

# Create FEEDBACK table
cursor.execute("""
CREATE TABLE feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    comment TEXT,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);
""")

conn.commit()
conn.close()

print("✅ All tables created successfully in suems.db")
