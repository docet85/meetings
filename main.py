from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

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
    models.seed()
except:  # this is nasty, but again it's just to have some data out of nothing
    pass


app.config['DEBUG'] = True

app.run()
