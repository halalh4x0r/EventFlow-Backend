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
class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return [u.to_dict() for u in users], 200
        
    def post(self):
        data = request.get_json()
        if not data.get("username") or not data.get("email"):
            return {"error": "username and email required"}, 400

        user = User(username=data["username"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


class UserDetailResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user.to_dict(), 200

    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()

        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]

        db.session.commit()
        return user.to_dict(), 200

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200


# ---------------- EVENTS ----------------
class EventsResource(Resource):
    def get(self):
        events = Event.query.all()
        return [e.to_dict() for e in events], 200

    def post(self):
        data = request.get_json()

        event = Event(
            title=data.get("title"),
            description=data.get("description"),
            location=data.get("location"),
            date_time=datetime.fromisoformat(data["date_time"]) 
                if data.get("date_time") else None,
            host_id=data.get("host_id"),
            images=data.get("images") or []
        )

        db.session.add(event)
        db.session.commit()
        return event.to_dict(), 201


class EventDetailResource(Resource):
    def get(self, id):
        event = Event.query.get_or_404(id)
        return event.to_dict(), 200

    def patch(self, id):
        event = Event.query.get_or_404(id)
        data = request.get_json()

        for field in ["title", "description", "location", "images"]:
            if field in data:
                setattr(event, field, data[field])

        if "date_time" in data:
            event.date_time = datetime.fromisoformat(data["date_time"])

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
        rsvps = RSVP.query.all()
        return [r.to_dict() for r in rsvps], 200

    def post(self):
        data = request.get_json()
        rsvp = RSVP(
            user_id=data.get("user_id"),
            event_id=data.get("event_id")
        )
        db.session.add(rsvp)
        db.session.commit()
        return rsvp.to_dict(), 201


class RsvpDetailResource(Resource):
    def patch(self, id):
        rsvp = RSVP.query.get_or_404(id)
        data = request.get_json()

        if "user_id" in data:
            rsvp.user_id = data["user_id"]
        if "event_id" in data:
            rsvp.event_id = data["event_id"]

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


class CommentDetailResource(Resource):
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


# ---------------- ROUTES REGISTRATION ----------------
api.add_resource(UsersResource, '/users')
api.add_resource(UserDetailResource, '/users/<int:id>')

api.add_resource(EventsResource, '/events')
api.add_resource(EventDetailResource, '/events/<int:id>')

api.add_resource(RsvpsResource, '/rsvps')
api.add_resource(RsvpDetailResource, '/rsvps/<int:id>')

api.add_resource(CommentsResource, '/comments')
api.add_resource(CommentDetailResource, '/comments/<int:id>')


if __name__ == "__main__":
    app.run(debug=True)
