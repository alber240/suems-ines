import sqlite3

conn = sqlite3.connect("suems.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(event_id) REFERENCES events(event_id),
    UNIQUE(user_id, event_id)
);
""")

conn.commit()
conn.close()

print("✅ registrations table created or already exists.")
