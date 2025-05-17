import sqlite3

conn = sqlite3.connect("suems.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE events ADD COLUMN target_roles TEXT;")
except sqlite3.OperationalError:
    print("Column 'target_roles' already exists.")

try:
    cursor.execute("ALTER TABLE events ADD COLUMN faculty TEXT;")
except sqlite3.OperationalError:
    print("Column 'faculty' already exists.")

try:
    cursor.execute("ALTER TABLE events ADD COLUMN department TEXT;")
except sqlite3.OperationalError:
    print("Column 'department' already exists.")

try:
    cursor.execute("ALTER TABLE events ADD COLUMN nationality TEXT;")
except sqlite3.OperationalError:
    print("Column 'nationality' already exists.")

conn.commit()
conn.close()

print("✅ Events table updated.")
