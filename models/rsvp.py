from . import db

class RSVP(db.Model):
    __tablename__ = "rsvps"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False, default="pending")  # give a default
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="rsvps")
    event = db.relationship("Event", back_populates="rsvps")

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "user_id": self.user_id,
            "event_id": self.event_id
        }
