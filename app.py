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



# ---------------- USERS ----------------
class UserListResource(Resource):

    def get(self):
        users = User.query.all()
        return [ u.to_dict() for u in users], 200
        
    def post(self):
        data=User.query.all()
        if not data.get("username") or not data.get("email"):
            return{"error":"username and email required"},400
        user = User(username=data["username"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        return (user.to_dict()), 201

    def patch(self):
        user = User.query.get_or_404(id)
        data = request.get_json()
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        db.session.commit()
        return (user.to_dict())

    def delete(self):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

# ---------------- EVENTS ----------------
class EventResource(Resource):
    def get(self,id):
       events = Event.query.all()
       return([e.to_dict() for e in events]) 



    def post():
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
        return(event.to_dict()), 201
    def patch(id):
        event = Event.query.get_or_404(id)
        data = request.get_json()
        for field in ["title", "description", "location", "start_time", "end_time"]:
            if field in data:
                setattr(event, field, data[field])
        db.session.commit()
        return (event.to_dict())
    def delete(id):
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}, 200



if __name__ == "__main__":
    app.run(debug=True)
