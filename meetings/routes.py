from flask import render_template


def create_routes(app):

    @app.route("/")
    def home():
        from meetings.models import Meeting, Person
        latest_meeting = Meeting.query.order_by(Meeting.ts.desc()).first()
        persons = Person.query.all()
        if latest_meeting is None or not latest_meeting.ongoing:
            ongoing = False
        return render_template('home.jinja2', latest_meeting=latest_meeting, ongoing=ongoing, persons=persons)

    @app.route("/hist")
    def hist():
        from meetings.models import Meeting
        return render_template('hist.jinja2', query_results=Meeting.query.paginate(per_page=5))
