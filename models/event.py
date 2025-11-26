from . import db

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    location = db.Column(db.String)
    date = db.Column(db.String, nullable=False)

    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationships
    organizer = db.relationship("User", back_populates="events")
    rsvps = db.relationship("RSVP", back_populates="event", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="event", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "date": self.date,
            "organizer_id": self.organizer_id
        }
