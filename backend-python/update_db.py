import sqlite3

conn = sqlite3.connect("suems.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN registration_no TEXT UNIQUE;")
except sqlite3.OperationalError:
    print("Column registration_no might already exist.")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN faculty TEXT;")
except sqlite3.OperationalError:
    print("Column faculty might already exist.")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN department TEXT;")
except sqlite3.OperationalError:
    print("Column department might already exist.")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN nationality TEXT CHECK(nationality IN ('Local', 'International'));")
except sqlite3.OperationalError:
    print("Column nationality might already exist.")

conn.commit()
conn.close()

print("Database updated with new columns.")
