"""Database models for the Bull application."""

from flask_sqlalchemy import SQLAlchemy
from app.database import Base

db = SQLAlchemy()

class User(Base):
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


class Story(Base):

    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    story_text = db.Column(db.String)
    faq = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    '''
    handles how the db entry is printed if it needs to be
    '''
    def __repr__(self):
        return '<Post %r>' % (self.story_text)

# class Question(Base):
#
#     __tablename__ = 'question'
#
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.String)
#     answer = db.Column(db.String)
#     story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
#
#     def __repr__(self):
#         return '<Post %r + %r>' % (self.question, self.answer)

class n2nModel(Base):

    __tablename__ = 'n2nModel'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
    saved_model_name = db.Column(db.Integer)
    access_key = db.Column(db.String)

    def __repr__(self):
        return '<Post %r>' % (self.id)
