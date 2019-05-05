from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from time import sleep

# We instantiate the webapp
import meetings

if meetings.app is None:
    app = Flask('Presenter')
    meetings.app = app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./presenter.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # Then let's do some DB stuff
    meetings.db = SQLAlchemy(app)

    from meetings.models import *
    from meetings.routes import create_routes

    Bootstrap(app)

    create_routes(app)

if __name__ == '__main__':
    # Since this is just a demo let's drop all and try to create everything
    meetings.db.drop_all()
    meetings.db.create_all()
    seed()
    meetings.app.config['DEBUG'] = True
    meetings.app.run(host="0.0.0.0", port="5000")
