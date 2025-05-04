from app import db
from datetime import time
import enum

class DayOfWeek(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class AvailabilitySlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    timezone = db.Column(db.String(100), nullable=False)

    # foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Availability {self.day_of_week} {self.start_time}-{self.end_time} ({self.timezone})>"
