from flask import render_template, request, make_response
from meetings.models import Meeting, Person, inclusion
from meetings import db


def create_routes(app):

    @app.route("/")
    def home():
        """ This is the main page - here we select the persons and let the meeting start or stop it when
        done.
        """
        ongoing = True
        latest_meeting = Meeting.query.order_by(Meeting.start_ts.desc()).first()
        persons = Person.query.all()
        if latest_meeting is None or not latest_meeting.ongoing:
            ongoing = False
            ongoing_participants = [p.id for p in persons if p.available]
        else:
            ongoing_participants = [p.id for p in latest_meeting.participants]

        return render_template('home.jinja2', latest_meeting=latest_meeting, ongoing=ongoing, persons=persons,
                               ongoing_participants=ongoing_participants)

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
        return make_response(200, 'ok')

    @app.route("/api/start_meeting", methods=['POST'])
    def start_meeting():
        from datetime import datetime
        m = Meeting.query.order_by(Meeting.start_ts.desc()).first()
        m.start = datetime.now()
        m.ongoing = True
        # db.session.add(m)
        db.session.commit()
        return make_response(200, 'ok')

    @app.route("/api/stop_meeting", methods=['POST'])
    def stop_meeting():
        from datetime import datetime
        m = Meeting.query.order_by(Meeting.start_ts.desc()).first()
        m.stop = datetime.now()
        m.ongoing = False
        # db.session.add(m)
        db.session.commit()
        return make_response(200, 'ok')

    @app.route("/api/person", methods=['POST'])
    def person():
        j_person = request.json
        p = Person(**j_person)
        db.session.add(p)
        db.session.commit()
        return make_response(200, 'ok')

    @app.route("/api/participant/<meeting_id>/<person_id>", methods=['POST', 'DELETE'])
    def participant(meeting_id, person_id):
        if request.method == 'POST':
            inclusion.insert().values(person_id=person_id, meeting_id=meeting_id)
        else:
            inclusion.delete().where(person_id=person_id, meeting_id=meeting_id)
        return make_response(200, 'ok')
