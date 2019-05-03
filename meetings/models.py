from datetime import datetime

from meetings import db, app

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=lambda: True)


presence = db.Table('presence',
                    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
                    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
                    )


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    presenter = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    ongoing = db.Column(db.Boolean, nullable=False, default=lambda: True)

    participants = db.relationship('Person', secondary=presence, lazy='subquery',
                                   backref=db.backref('meetings', lazy=True))


class AvailabilityEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=lambda: False)

    person = db.relationship('Person', backref=db.backref('person', lazy=True))


def seed():
    from random import randint, random
    from time import sleep
    names = ['Jane', 'Jack', 'John', 'Jill', 'Jade', 'Jim', 'Jes']
    surnames = ['Doe', 'Dam', 'Der', 'Dew', 'Dat', 'Dow', 'Dyl']
    ppl = 0
    while ppl < 10:
        name = names[randint(0, 6)] + ' ' + surnames[randint(0, 6)]
        if Person.query.filter_by(username=name).first():
            continue
        new_user = Person(username=name, available=(random() < 0.7))
        db.session.add(new_user)
        db.session.commit()
        ppl += 1

    db.session.flush()