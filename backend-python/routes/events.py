from flask import Blueprint, jsonify
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
