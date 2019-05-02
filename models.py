from datetime import datetime

from sqlalchemy import text

from main import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=lambda: False)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    presenter_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)


class AvailabilityEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=lambda: False)
    person = db.relationship('Person', backref=db.backref('persons', lazy=True))

def seed(db):
    names = ['Jane', 'Jack', 'John', 'Jill', 'Jade', 'Jim', 'Jes']
    surnames = ['Doe', 'Dam', 'Der', 'Dew', 'Dat', 'Dow', 'Dyl']
    ppl = 0
    while ppl < 10:
        uname =
        Person(username=)
