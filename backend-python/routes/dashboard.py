from flask import Blueprint, jsonify
import sqlite3

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/api/dashboard', methods=['GET'])
def get_dashboard_stats():
    conn = sqlite3.connect("suems.db")
    cursor = conn.cursor()

    # Total users by role
    cursor.execute("""
        SELECT role, COUNT(*) FROM users GROUP BY role
    """)
    users_by_role = dict(cursor.fetchall())

    # Total events
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    # Registrations per event
    cursor.execute("""
        SELECT e.event_id, e.title, COUNT(r.registration_id) 
        FROM events e
        LEFT JOIN registrations r ON e.event_id = r.event_id
        GROUP BY e.event_id
    """)
    registrations = [
        {"event_id": row[0], "title": row[1], "registration_count": row[2]}
        for row in cursor.fetchall()
    ]

    # Attendance summaries per event
    cursor.execute("""
        SELECT e.event_id, e.title,
        SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
        SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_count
        FROM events e
        LEFT JOIN attendance a ON e.event_id = a.event_id
        GROUP BY e.event_id
    """)
    attendance_summary = [
        {
            "event_id": row[0],
            "title": row[1],
            "present": row[2] or 0,
            "absent": row[3] or 0
        }
        for row in cursor.fetchall()
    ]

    conn.close()

    return jsonify({
        "users_by_role": users_by_role,
        "total_events": total_events,
        "registrations": registrations,
        "attendance_summary": attendance_summary
    })
