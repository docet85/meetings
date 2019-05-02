from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from time import sleep

# We instantiate the webapp
app = Flask('Presenter')

# Then let's do some DB stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)

import models
import routes

# Since this is just a demo let's drop all and try to create everything
try:
    db.drop_all()
    db.create_all()
    sleep(2)
    models.seed()
except Exception as e:  # this is nasty, but again it's just to have some data out of nothing
    app.logger.warning(e)


app.config['DEBUG'] = True

app.run()
