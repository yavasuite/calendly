from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meeting import Meeting
from app import db
from datetime import datetime

meeting_bp = Blueprint("meeting", __name__, url_prefix="/api/meetings")

@meeting_bp.route("/schedule", methods=["POST"])
@jwt_required()
def schedule_meeting():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description", "")
    start = data.get("start_time")
    end = data.get("end_time")

    # Validate input
    if not all([title, start, end]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        start_time = datetime.fromisoformat(start)
        end_time = datetime.fromisoformat(end)
    except ValueError:
        return jsonify({"error": "Datetime format must be ISO format (e.g., 2025-03-22T14:00:00)"}), 400

    if start_time >= end_time:
        return jsonify({"error": "Start time must be before end time"}), 400

    user_id = int(get_jwt_identity())

    meeting = Meeting(
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
        user_id=user_id
    )

    db.session.add(meeting)
    db.session.commit()

    return jsonify({
        "id": meeting.id,
        "title": meeting.title,
        "description": meeting.description,
        "start_time": meeting.start_time.isoformat(),
        "end_time": meeting.end_time.isoformat()
    }), 201
