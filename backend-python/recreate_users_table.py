import sqlite3

conn = sqlite3.connect("suems.db")
cursor = conn.cursor()

try:
    # Create new table with full schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users_new (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        registration_no TEXT UNIQUE,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        nationality TEXT CHECK(nationality IN ('Local', 'International')),
        faculty TEXT,
        department TEXT
    );
    """)

    # Copy data from old table to new table (only existing columns)
    cursor.execute("""
    INSERT INTO users_new (user_id, name, email, phone, password, role)
    SELECT user_id, name, email, phone, password, role FROM users;
    """)

    # Drop old table
    cursor.execute("DROP TABLE users;")

    # Rename new table to old name
    cursor.execute("ALTER TABLE users_new RENAME TO users;")

    conn.commit()
    print("✅ Recreated users table with updated schema.")
except Exception as e:
    print("⚠️ Error:", e)
finally:
    conn.close()
