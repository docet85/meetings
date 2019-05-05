from flask import render_template, request, make_response
from meetings.models import Meeting, Person, Event
from meetings import db


def create_routes(app):

    @app.route("/")
    def home():
        """ This is the main page - here we select the persons and let the meeting start or stop it when
        done.
        """
        latest_meeting = Meeting.query.order_by(Meeting.creation_ts.desc()).first()
        persons = Person.query.all()
        if latest_meeting is None:
            status = 'finished'
            meeting_id = None
        else:
            meeting_id = latest_meeting.id
            status = latest_meeting.status
        if status in ['created', 'started']:
            ongoing_participants = [p.id for p in latest_meeting.participants]
        else:
            ongoing_participants = [p.id for p in persons if p.available]

        return render_template('home.jinja2', latest_meeting=latest_meeting, status=status, persons=persons,
                               ongoing_participants=ongoing_participants, meeting_id=meeting_id)

    @app.route("/hist")
    def hist():
        """
        The history page, displaying the info log
        """
        e_info = [
            {
                'label': 'Meeting created',
                'class': 'primary'
            },
            {
                'label': 'Meeting start',
                'class': 'success'
            },
            {
                'label': 'Meeting finish',
                'class': 'danger'
            },
            {
                'label': 'New Person created',
                'class': 'info'
            },
            {
                'label': 'Person now available',
                'class': 'light'
            },
            {
                'label': 'Person missing',
                'class': 'active'
            },
            {
                'label': 'Person Invited',
                'class': 'warning'
            },
            {
                'label': 'Person Excluded',
                'class': 'dark'
            },
        ]
        return render_template('hist.jinja2', events=Event.query.order_by(Event.ts.desc()).paginate(per_page=10),
                               e_info=e_info)

    # ########################## API ############################ #

    @app.route("/api/create_meeting", methods=['POST'])
    def create_meeting():
        m = Meeting()
        m.participants = [p for p in Person.query.filter_by(available=True).all()]
        db.session.add(m)
        db.session.commit()
        log_event(0, mid=m.id)
        return make_response('ok', 200)

    @app.route("/api/start_meeting", methods=['POST'])
    def start_meeting():
        from datetime import datetime
        from random import choice
        m = Meeting.query.order_by(Meeting.creation_ts.desc()).first()
        m.start_ts = datetime.now()
        m.status = 'started'

        p_ids = [p.id for p in m.participants]

        m.presenter_id = choice(p_ids)

        db.session.commit()
        log_event(1, mid=m.id)
        return make_response('ok', 200)

    @app.route("/api/stop_meeting", methods=['POST'])
    def stop_meeting():
        from datetime import datetime
        m = Meeting.query.order_by(Meeting.creation_ts.desc()).first()
        m.stop_ts = datetime.now()
        m.status = 'finished'

        db.session.commit()
        log_event(2, mid=m.id)
        return make_response('ok', 200)

    @app.route("/api/person/<uname>", methods=['POST'])
    def person(uname):
        import json
        j_person = {'username': uname}
        p = Person(**j_person)
        db.session.add(p)
        db.session.commit()
        log_event(3, pid=p.id)
        return make_response(json.dumps(p.to_dict()), 200)

    @app.route("/api/person/presence/<pid>", methods=['POST', 'DELETE'])
    def person_presence(pid):
        p = Person.query.filter_by(id=pid).first_or_404()
        p.available = (request.method == 'POST')
        db.session.commit()
        e_code = 5
        if p.available:
            e_code = 4
        log_event(e_code, pid=p.id)
        return make_response('ok', 200)

    @app.route("/api/participant/<meeting_id>/<person_id>", methods=['POST', 'DELETE'])
    def participant(meeting_id, person_id):
        m = Meeting.query.filter_by(id=meeting_id).first()
        p = Person.query.filter_by(id=person_id).first()
        if not m or not p:
            return make_response('Meeting or person not existing', 404)

        if request.method == 'POST':
            m.participants.append(p)
            e_code = 6
        else:
            m.participants.remove(p)
            e_code = 7
        db.session.commit()
        log_event(e_code, pid=p.id, mid=m.id)

        return make_response('ok', 200)


def log_event(e_code, pid=None, mid=None):
    try:
        e = Event(event_code=e_code, meeting_id=mid, person_id=pid)
        db.session.add(e)
        db.session.commit()
    except:
        print("Event logging failed")