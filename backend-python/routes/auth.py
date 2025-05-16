from flask import Blueprint, request, jsonify
import sqlite3

auth = Blueprint('auth', __name__)

@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role', 'Student')

    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, password, role)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists."}), 409
    finally:
        conn.close()

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user_id": user[0], "role": user[5]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
