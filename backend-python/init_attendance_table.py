import sqlite3

conn = sqlite3.connect("suems.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent')) NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(event_id) REFERENCES events(event_id),
    UNIQUE(user_id, event_id)
);
""")

conn.commit()
conn.close()
print("✅ attendance table created or already exists.")
