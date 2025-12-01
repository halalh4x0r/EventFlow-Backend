from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from config import Config
from models import db, User, Event, RSVP, Comment

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

# ---------------- USERS ----------------
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [u.to_dict() for u in users], 200

    def post(self):
        data = request.get_json()
        if not data.get("username") or not data.get("email") or not data.get("password"):
            return {"error": "username, email, and password required"}, 400
        user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password")
        )
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


# ---------------- EVENTS ----------------
class EventResource(Resource):
    def get(self):
        events = Event.query.all()
        return [e.to_dict() for e in events], 200

    def post(self):
        data = request.get_json()
        event = Event(
            title=data.get("title"),
            description=data.get("description"),
            location=data.get("location"),
            date_time=datetime.fromisoformat(data["date_time"]) if data.get("date_time") else None,
            host_id=data.get("host_id"),
            images=data.get("images") or []
        )
        db.session.add(event)
        db.session.commit()
        return event.to_dict(), 201


class EventDetailResource(Resource):
    def get(self, id):
        event = Event.query.get(id)
        if not event:
            return {"error": "Event not found"}, 404
        return event.to_dict(), 200

    def patch(self, id):
        event = Event.query.get_or_404(id)
        data = request.get_json()
        if "title" in data:
            event.title = data["title"]
        if "description" in data:
            event.description = data["description"]
        if "location" in data:
            event.location = data["location"]
        if "date_time" in data:
            event.date_time = datetime.fromisoformat(data["date_time"])
        if "images" in data:
            event.images = data["images"]
        db.session.commit()
        return event.to_dict(), 200

    def delete(self, id):
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}, 200


# ---------------- RSVPS ----------------
class RsvpsResource(Resource):
    def get(self):
        event_id = request.args.get("event_id")
        if event_id:
            rsvps = RSVP.query.filter_by(event_id=event_id).all()
        else:
            rsvps = RSVP.query.all()
        return [r.to_dict() for r in rsvps], 200

    def post(self):
        data = request.get_json()
        rsvp = RSVP(
            user_id=data.get("user_id"),
            event_id=data.get("event_id"),
            status=data.get("status", "pending")
        )
        db.session.add(rsvp)
        db.session.commit()
        return rsvp.to_dict(), 201

    def patch(self, id):
        rsvp = RSVP.query.get_or_404(id)
        data = request.get_json()
        for field in ["user_id", "event_id", "status"]:
            if field in data:
                setattr(rsvp, field, data[field])
        db.session.commit()
        return rsvp.to_dict(), 200

    def delete(self, id):
        rsvp = RSVP.query.get_or_404(id)
        db.session.delete(rsvp)
        db.session.commit()
        return {"message": "RSVP deleted"}, 200


# ---------------- COMMENTS ----------------
class CommentsResource(Resource):
    def get(self):
        event_id = request.args.get("event_id")
        if event_id:
            comments = Comment.query.filter_by(event_id=event_id).all()
        else:
            comments = Comment.query.all()
        return [c.to_dict() for c in comments], 200

    def post(self):
        data = request.get_json()
        comment = Comment(
            user_id=data.get("user_id"),
            event_id=data.get("event_id"),
            content=data.get("content")
        )
        db.session.add(comment)
        db.session.commit()
        return comment.to_dict(), 201

    def patch(self, id):
        comment = Comment.query.get_or_404(id)
        data = request.get_json()
        for field in ["user_id", "event_id", "content"]:
            if field in data:
                setattr(comment, field, data[field])
        db.session.commit()
        return comment.to_dict(), 200

    def delete(self, id):
        comment = Comment.query.get_or_404(id)
        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted"}, 200


# ---------------- REGISTER RESOURCES ----------------
api.add_resource(UserListResource, '/users')
api.add_resource(EventResource, '/events')
api.add_resource(EventDetailResource, '/events/<int:id>')
api.add_resource(RsvpsResource, '/rsvps', '/rsvps/<int:id>')
api.add_resource(CommentsResource, '/comments', '/comments/<int:id>')


if __name__ == "__main__":
    app.run(debug=True)
