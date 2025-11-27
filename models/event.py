from sqlalchemy.dialects.sqlite import JSON
from . import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    location = db.Column(db.String)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    images = db.Column(JSON)  # <-- add this

    # Relationships
    organizer = db.relationship(
        "User",
        back_populates="events",
        foreign_keys=[organizer_id]
    )
    rsvps = db.relationship("RSVP", back_populates="event", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="event", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "organizer_id": self.organizer_id,
            "images": self.images or []  # return an empty list if None
        }
