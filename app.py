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




