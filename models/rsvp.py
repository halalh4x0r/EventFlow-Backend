from config import db

class RSVP(db.Model):
    __tablename__ = "rsvps"
    id = db.Column(db.Integer, primary_key=True)
