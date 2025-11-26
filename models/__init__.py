from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .event import Event
from .rsvp import RSVP
from .comment import Comment
