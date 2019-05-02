from flask import render_template

from main import app

@app.route("/")
def home():
    return render_template('home.jinja2')


@app.route("/hist")
def hist():
    from models import Person
    return render_template('hist.jinja2', query_results=Person.query.filter_by(available=True).paginate())
