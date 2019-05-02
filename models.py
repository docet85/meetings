from datetime import datetime

from sqlalchemy import text

from main import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=lambda: True)


presence = db.Table('presences',
                    db.Column('person_id', db.Integer, db.ForeignKey('persons.id'), primary_key=True),
                    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'), primary_key=True)
                    )


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    presenter = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)

    partecipants = db.relationship('Person', secondary=presence, lazy='subquery',
                                   backref=db.backref('meetingss', lazy=True))


class AvailabilityEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=lambda: False)

    # person = db.relationship('Person', backref=db.backref('persons', lazy=True))




def seed():
    from random import randint
    names = ['Jane', 'Jack', 'John', 'Jill', 'Jade', 'Jim', 'Jes']
    surnames = ['Doe', 'Dam', 'Der', 'Dew', 'Dat', 'Dow', 'Dyl']
    ppl = 0
    while ppl < 10:
        name = names[randint(0, 6)] + surnames[randint(0, 6)]
        try:
            new_user = Person(username=name)
            db.session.add(new_user)
            db.session.commit()
            ppl += 1
        except Exception as e:
            # this in case we get collisions
            from main import app
            app.logger.warning(e)
