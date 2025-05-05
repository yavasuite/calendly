from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.meeting import Meeting, MeetingStatus
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

    # Check for conflicts (any meeting that overlaps the requested time)
    conflict = Meeting.query.filter(
        Meeting.user_id == user_id,
        Meeting.start_time < end_time,
        Meeting.end_time > start_time
    ).first()

    if conflict:
        return jsonify({"error": "Time slot already booked"}), 409

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

@meeting_bp.route("/<int:meeting_id>/reschedule", methods=["PATCH"])
@jwt_required()
def reschedule_meeting(meeting_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    new_start = data.get("start_time")
    new_end = data.get("end_time")

    if not all([new_start, new_end]):
        return jsonify({"error": "Missing start_time or end_time"}), 400

    try:
        start_time = datetime.fromisoformat(new_start)
        end_time = datetime.fromisoformat(new_end)
    except ValueError:
        return jsonify({"error": "Datetime must be in ISO format"}), 400

    if start_time >= end_time:
        return jsonify({"error": "start_time must be before end_time"}), 400

    meeting = Meeting.query.filter_by(id=meeting_id, user_id=user_id).first()
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    # Check for conflicts with other meetings
    conflict = Meeting.query.filter(
        Meeting.user_id == user_id,
        Meeting.id != meeting_id,
        Meeting.start_time < end_time,
        Meeting.end_time > start_time
    ).first()

    if conflict:
        return jsonify({"error": "New time slot conflicts with an existing meeting"}), 409

    meeting.start_time = start_time
    meeting.end_time = end_time

    db.session.commit()

    return jsonify({
        "id": meeting.id,
        "title": meeting.title,
        "description": meeting.description,
        "start_time": meeting.start_time.isoformat(),
        "end_time": meeting.end_time.isoformat()
    }), 200

@meeting_bp.route("/<int:meeting_id>", methods=["DELETE"])
@jwt_required()
def cancel_meeting(meeting_id):
    user_id = int(get_jwt_identity())

    meeting = Meeting.query.filter_by(id=meeting_id, user_id=user_id).first()
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    meeting.status = MeetingStatus.CANCELED
    db.session.commit()

    return jsonify({"message": f"Meeting {meeting_id} canceled successfully."}), 200

@meeting_bp.route("", methods=["GET"])
@jwt_required()
def list_meetings():
    user_id = int(get_jwt_identity())

    meetings = Meeting.query.filter_by(
        user_id=user_id,
        status=MeetingStatus.SCHEDULED
    ).order_by(Meeting.start_time).all()

    return jsonify([
        {
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "start_time": m.start_time.isoformat(),
            "end_time": m.end_time.isoformat(),
            "status": m.status.value
        } for m in meetings
    ]), 200
