from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from models import User, Story, Question, n2nModel
from werkzeug.utils import secure_filename
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print APP_ROOT

STORY_UPLOAD_FOLDER = 'data/uploads/story'
QUESTION_UPLOAD_FOLDER = 'data/uploads/question'
ANSWER_UPLOAD_FOLDER = 'data/uploads/answer'

print
app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/app.db'

db = SQLAlchemy(app)
db.create_all()

##TODO find a better way to separate this code
class User(db.Model):
    """An admin user capable of viewing reports.
    :param str email: email address of user
    :param str password: encrypted password for the user
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satify Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return '<User %r>' % (self.name)

class Story(db.Model):

    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    story_text = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    '''
    handles how the db entry is printed if it needs to be
    '''
    def __repr__(self):
        return '<Post %r>' % (self.story_text)

class Question(db.Model):

    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))

    def __repr__(self):
        return '<Post %r + %r>' % (self.question, self.answer)

class n2nModel(db.Model):

    __tablename__ = 'n2nmodel'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))

    def __repr__(self):
        return '<Post %r>' % (self.id)

from app import views
