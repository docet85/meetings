from datetime import datetime

from meetings import db

"""
For sake of implementation these are persistency-centered models: they contain all the information but have no method 
and perform no "action". All the behavior is coded inside so.called "routes", that act de-facto like controllers.
"""


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=lambda: True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'available': self.available
        }


invitation = db.Table('invitation',
                     db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
                     db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
                     )


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    start_ts = db.Column(db.DateTime, nullable=True)
    stop_ts = db.Column(db.DateTime, nullable=True)
    presenter_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    status = db.Column(db.String, nullable=False, default='created')

    # relations are handy to retrieve the whole related object/set of related object without querying directly for them
    presenter = db.relationship('Person', primaryjoin='Meeting.presenter_id == Person.id')
    participants = db.relationship('Person', secondary=invitation, lazy='subquery',
                                   backref=db.backref('meetings', lazy=True))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)

    """  for simplicity and extendability no enum but int - there should be a static table with definitions - but for a
         demo hardcoded values are enough.
         1 - meeting start
         2 - meeting stop
         3 - person added
         4 - person missing
         5 - person available
         6 - person added to meeting
         7 - person removed from meeting
         """


def seed(n_users=10):
    """
    Convenience method generating users. Max 49 unique names are available.
    :return:
    """
    from random import randint, random

    if n_users > 49 or n_users <= 0:
        raise ValueError("The number of users to seed should be greater than 0 and lower than 50")

    names = ['Jane', 'Jack', 'John', 'Jill', 'Jade', 'Jim', 'Jes']
    surnames = ['Doe', 'Dam', 'Der', 'Dew', 'Dat', 'Dow', 'Dyl']
    ppl = 0
    while ppl < n_users:
        name = names[randint(0, 6)] + ' ' + surnames[randint(0, 6)]
        if Person.query.filter_by(username=name).first():
            continue
        new_user = Person(username=name, available=(random() < 0.7))
        db.session.add(new_user)
        db.session.commit()
        ppl += 1
