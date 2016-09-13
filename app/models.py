"""Database models for the Bull application."""

import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    '''
    handles how the db entry is printed if it needs to be
    '''
    def __repr__(self):
        return '<Post %r>' % (self.body)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))

    def __repr__(self):
        return '<Post %r + %r>' % (self.question, self.answer)

class n2nModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))

    def __repr__(self):
        return '<Post %r>' % (self.id)
