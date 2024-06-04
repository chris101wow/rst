from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    duration = db.Column(db.Integer)
    timeh = db.Column(db.Integer)
    timem = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    Schedule = db.relationship('Schedule')