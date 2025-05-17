import sqlite3

conn = sqlite3.connect("suems.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    INSERT INTO users 
    (name, registration_no, email, phone, password, role, nationality, faculty, department)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Test Student",
        "STU2025001",
        "teststudent@example.com",
        "0781234567",
        "password123",
        "Student",
        "Local",
        "Science",
        "Biotech"
    ))
    conn.commit()
    print("✅ Test user added successfully.")
except sqlite3.IntegrityError as e:
    print(f"⚠️ Could not add user: {e}")
finally:
    conn.close()
