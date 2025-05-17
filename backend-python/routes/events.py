from flask import Blueprint, request, jsonify
import sqlite3

events = Blueprint('events', __name__)

@events.route('/api/events', methods=['GET'])
def get_events():
    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()
    cursor.execute("SELECT event_id, title, location, date FROM events")
    rows = cursor.fetchall()
    conn.close()

    event_list = []
    for row in rows:
        event_list.append({
            "event_id": row[0],
            "title": row[1],
            "location": row[2],
            "date": row[3]
        })

    return jsonify(event_list)

# ✅ NEW: Create Event Route (POST)
@events.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    event_type = data.get('event_type', 'Other')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    target_roles = data.get('target_roles')
    faculty = data.get('faculty')
    department = data.get('department')
    nationality = data.get('nationality')

    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO events 
            (title, description, location, event_type, date, start_time, end_time, target_roles, faculty, department, nationality)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, description, location, event_type,
            date, start_time, end_time,
            target_roles, faculty, department, nationality
        ))
        conn.commit()
        return jsonify({"message": "Event created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()
        conn.close()

@events.route('/api/events/<int:event_id>/register', methods=['POST'])
def register_for_event(event_id):
    data = request.get_json()
    user_id = data.get('user_id')

    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()

    # 1. Get user details
    cursor.execute("""
        SELECT role, faculty, department, nationality 
        FROM users WHERE user_id = ?
    """, (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found."}), 404

    user_role, user_faculty, user_department, user_nationality = user

    # 2. Get event eligibility
    cursor.execute("""
        SELECT target_roles, faculty, department, nationality 
        FROM events WHERE event_id = ?
    """, (event_id,))
    event = cursor.fetchone()
    if not event:
        conn.close()
        return jsonify({"error": "Event not found."}), 404

    target_roles, target_faculty, target_department, target_nationality = event

    # 3. Eligibility checks
    if target_roles and target_roles != user_role:
        return jsonify({"error": f"This event is for {target_roles} only."}), 403

    if target_faculty and target_faculty != user_faculty:
        return jsonify({"error": f"This event is only for Faculty of {target_faculty}."}), 403

    if target_department and target_department != user_department:
        return jsonify({"error": f"This event is only for {target_department} department."}), 403

    if target_nationality and target_nationality != user_nationality:
        return jsonify({"error": f"This event is only for {target_nationality} participants."}), 403

    # 4. Register
    try:
        cursor.execute("""
            INSERT INTO registrations (user_id, event_id)
            VALUES (?, ?)
        """, (user_id, event_id))
        conn.commit()
        return jsonify({"message": "Successfully registered for the event."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Already registered for this event."}), 409
    finally:
        conn.close()

@events.route('/api/events/<int:event_id>/attendance', methods=['POST'])
def mark_attendance(event_id):
    data = request.get_json()
    user_id = data.get('user_id')
    status = data.get('status')

    if status not in ['Present', 'Absent']:
        return jsonify({"error": "Invalid status. Use 'Present' or 'Absent'."}), 400

    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO attendance (user_id, event_id, status)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, event_id) DO UPDATE SET status = excluded.status, timestamp = CURRENT_TIMESTAMP
        """, (user_id, event_id, status))
        conn.commit()
        return jsonify({"message": f"{status} marked for user {user_id}."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

## viwe attendance logs
@events.route('/api/events/<int:event_id>/attendance', methods=['GET'])
def get_attendance_log(event_id):
    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.user_id, u.name, u.email, u.role, a.status, a.timestamp
    FROM attendance a
    JOIN users u ON a.user_id = u.user_id
    WHERE a.event_id = ?
    """, (event_id,))
    rows = cursor.fetchall()
    conn.close()

    attendance_list = []
    for row in rows:
        attendance_list.append({
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[3],
            "status": row[4],
            "timestamp": row[5]
        })

    return jsonify(attendance_list)


        

