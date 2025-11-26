from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from models import db, User, Event, RSVP, Comment

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Initialize migrations (THIS was missing)
migrate = Migrate(app, db)

@app.route("/")
def index():
    return {"message": "EventFlow API running..."}

# ---------- USERS ROUTE ----------
@app.route("/users")
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# ---------- EVENTS ROUTE ----------
@app.route("/events")
def get_events():
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events])

# ---------- RSVPS ROUTE ----------
@app.route("/rsvps")
def get_rsvps():
    rsvps = RSVP.query.all()
    return jsonify([r.to_dict() for r in rsvps])

# ---------- COMMENTS ROUTE ----------
@app.route("/comments")
def get_comments():
    comments = Comment.query.all()
    return jsonify([c.to_dict() for c in comments])

if __name__ == "__main__":
    app.run(debug=True)
