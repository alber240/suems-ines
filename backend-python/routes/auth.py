from flask import Blueprint, request, jsonify
import sqlite3

auth = Blueprint('auth', __name__)

@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    registration_no = data.get('registration_no')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role', 'Student')
    nationality = data.get('nationality')
    faculty = data.get('faculty')
    department = data.get('department')

    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users 
            (name, registration_no, email, phone, password, role, nationality, faculty, department) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, registration_no, email, phone, password, role, nationality, faculty, department))
        conn.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: users.registration_no" in str(e):
            return jsonify({"error": "Registration number already exists."}), 409
        elif "UNIQUE constraint failed: users.email" in str(e):
            return jsonify({"error": "Email already exists."}), 409
        else:
            return jsonify({"error": "Registration failed."}), 400
    finally:
        conn.close()
