from flask import render_template, request, make_response
from meetings.models import Meeting, Person, invitation
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
        The history page, displaying the last meetings, and the exclusion log
        """
        return render_template('hist.jinja2', query_results=Meeting.query.paginate(per_page=5))

    # ########################## API ############################ #

    @app.route("/api/create_meeting", methods=['POST'])
    def create_meeting():
        m = Meeting()
        m.participants = [p for p in Person.query.filter_by(available=True).all()]
        db.session.add(m)
        db.session.commit()
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
        return make_response('ok', 200)

    @app.route("/api/stop_meeting", methods=['POST'])
    def stop_meeting():
        from datetime import datetime
        m = Meeting.query.order_by(Meeting.creation_ts.desc()).first()
        m.stop_ts = datetime.now()
        m.status = 'finished'

        db.session.commit()
        return make_response('ok', 200)

    @app.route("/api/person/<uname>", methods=['POST'])
    def person(uname):
        import json
        j_person = {'username': uname}
        p = Person(**j_person)
        db.session.add(p)
        db.session.commit()
        return make_response(json.dumps(p.to_dict()), 200)

    @app.route("/api/person/presence/<pid>", methods=['POST', 'DELETE'])
    def person_presence(pid):
        p = Person.query.filter_by(id=pid).first_or_404()
        p.available = (request.method == 'POST')
        db.session.commit()
        return make_response('ok', 200)

    @app.route("/api/participant/<meeting_id>/<person_id>", methods=['POST', 'DELETE'])
    def participant(meeting_id, person_id):
        m = Meeting.query.filter_by(id=meeting_id).first()
        p = Person.query.filter_by(id=person_id).first()
        if not m or not p:
            return make_response('Meeting or person not existing', 404)

        if request.method == 'POST':
            m.participants.append(p)
        else:
            m.participants.remove(p)
        db.session.commit()
        return make_response('ok', 200)
