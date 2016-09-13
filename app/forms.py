# """Forms for the application."""
# from flask_wtf import Form
# from wtforms import TextField, PasswordField, SelectField
# from wtforms.validators import DataRequired
#
# from app import db
#
# class LoginForm(Form):
#     """Form class for user login."""
#     name = TextField('name', validators=[DataRequired()])
#     email = TextField('email', validators=[DataRequired()])
#     password = PasswordField('password', validators=[DataRequired()])
#
#     # def validate_on_submit():
#     #     return True
