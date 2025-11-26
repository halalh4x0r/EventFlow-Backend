from flask import Flask, jsonify, request
from config import Config
from models import db, User, Event, RSVP, Comment
from flask_migrate import Migrate
from flask_restful import Api, Resource

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
api=Api(app)

@app.route("/")
def index():
    return {"message": "EventFlow API running..."}

# ---------------- USERS ----------------
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("username") or not data.get("email"):
        return {"error": "username and email required"}, 400
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route("/users/<int:id>", methods=["PATCH"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    db.session.commit()
    return jsonify(user.to_dict())

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}, 200

# ---------------- EVENTS ----------------
@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events])

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    event = Event(
        title=data.get("title"),
        description=data.get("description"),
        location=data.get("location"),
        start_time=data.get("start_time"),
        end_time=data.get("end_time"),
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()
    for field in ["title", "description", "location", "start_time", "end_time"]:
        if field in data:
            setattr(event, field, data[field])
    db.session.commit()
    return jsonify(event.to_dict())

@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return {"message": "Event deleted"}, 200

# ---------------- RSVPS ----------------
@app.route("/rsvps", methods=["GET"])
def get_rsvps():
    rsvps = RSVP.query.all()
    return jsonify([r.to_dict() for r in rsvps])

@app.route("/rsvps", methods=["POST"])
def create_rsvp():
    data = request.get_json()
    rsvp = RSVP(user_id=data.get("user_id"), event_id=data.get("event_id"))
    db.session.add(rsvp)
    db.session.commit()
    return jsonify(rsvp.to_dict()), 201

@app.route("/rsvps/<int:id>", methods=["PATCH"])
def update_rsvp(id):
    rsvp = RSVP.query.get_or_404(id)
    data = request.get_json()
    for field in ["user_id", "event_id"]:
        if field in data:
            setattr(rsvp, field, data[field])
    db.session.commit()
    return jsonify(rsvp.to_dict())

@app.route("/rsvps/<int:id>", methods=["DELETE"])
def delete_rsvp(id):
    rsvp = RSVP.query.get_or_404(id)
    db.session.delete(rsvp)
    db.session.commit()
    return {"message": "RSVP deleted"}, 200

# ---------------- COMMENTS ----------------
@app.route("/comments", methods=["GET"])
def get_comments():
    comments = Comment.query.all()
    return jsonify([c.to_dict() for c in comments])

@app.route("/comments", methods=["POST"])
def create_comment():
    data = request.get_json()
    comment = Comment(user_id=data.get("user_id"),
                      event_id=data.get("event_id"),
                      content=data.get("content"))
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@app.route("/comments/<int:id>", methods=["PATCH"])
def update_comment(id):
    comment = Comment.query.get_or_404(id)
    data = request.get_json()
    for field in ["user_id", "event_id", "content"]:
        if field in data:
            setattr(comment, field, data[field])
    db.session.commit()
    return jsonify(comment.to_dict())

@app.route("/comments/<int:id>", methods=["DELETE"])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return {"message": "Comment deleted"}, 200

if __name__ == "__main__":
    app.run(debug=True)
