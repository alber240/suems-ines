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
