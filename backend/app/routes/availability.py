from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.availability import AvailabilitySlot, DayOfWeek
from app import db
from datetime import datetime

availability_bp = Blueprint("availability", __name__, url_prefix="/api/availability")


@availability_bp.route("", methods=["GET"])
@jwt_required()
def get_available_slots():
    user_id = int(get_jwt_identity())
    date_str = request.args.get("date")

    query = AvailabilitySlot.query.filter_by(user_id=user_id)

    if date_str:
        try:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        start_of_day = datetime.combine(query_date, datetime.min.time())
        end_of_day = datetime.combine(query_date, datetime.max.time())
        query = query.filter(
            AvailabilitySlot.start_time >= start_of_day,
            AvailabilitySlot.end_time <= end_of_day
        )

    slots = query.order_by(AvailabilitySlot.start_time).all()

    return jsonify([
        {
            "id": slot.id,
            "day_of_week": slot.day_of_week.value,
            "start_time": slot.start_time.isoformat(),
            "end_time": slot.end_time.isoformat(),
            "timezone": slot.timezone
        } for slot in slots
    ])


@availability_bp.route("", methods=["POST"])
@jwt_required()
def create_availability_slot():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")
    day_of_week_str = data.get("day_of_week")
    timezone = data.get("timezone")

    if not start_time_str or not end_time_str:
        return jsonify({"error": "start_time and end_time are required"}), 400
    if not day_of_week_str:
        return jsonify({"error": "day_of_week is required"}), 400

    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({"error": "Datetime format must be ISO (e.g., 2025-05-04T14:00:00)"}), 400

    if start_time >= end_time:
        return jsonify({"error": "start_time must be before end_time"}), 400

    try:
        day_of_week = DayOfWeek(day_of_week_str)
    except ValueError:
        return jsonify({"error": f"Invalid day_of_week: {day_of_week_str}. Must be one of {[d.value for d in DayOfWeek]}"}), 400

    slot = AvailabilitySlot(
        start_time=start_time,
        end_time=end_time,
        day_of_week=day_of_week,
        timezone=timezone,
        user_id=user_id
    )

    db.session.add(slot)
    db.session.commit()

    return jsonify({
        "id": slot.id,
        "day_of_week": slot.day_of_week.value,
        "start_time": slot.start_time.isoformat(),
        "end_time": slot.end_time.isoformat(),
        "timezone": slot.timezone
    }), 201
