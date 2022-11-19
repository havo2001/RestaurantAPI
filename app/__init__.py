from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


from app import models
from app import api
