from sqlalchemy.dialects.sqlite import JSON
from . import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    location = db.Column(db.String)
    date_time = db.Column(db.DateTime, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    images = db.Column(JSON)  # <-- add this

    # Relationships
    organizer = db.relationship(
        "User",
        back_populates="events",
        foreign_keys=[host_id]
    )
    rsvps = db.relationship("RSVP", back_populates="event", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="event", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "date_time": self.date_time.isoformat() if self.date_time else None,
            "host_id": self.host_id,
            "images": self.images or []  # return an empty list if None
        }
