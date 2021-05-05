"""Forms for notes app."""

from wtforms import StringField, SelectField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, length, email_validator, Email


class RegistrationForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField(
                        "Username:",
                        validators=[InputRequired(),
                                    length(max=20)])
    password = PasswordField("Password:",
                            validators=[InputRequired()])
    email = StringField("Email:",
                        validators=[InputRequired(),
                                    Email(),
                                    length(max=50)])
    first_name = StringField("First Name:",
                        validators=[InputRequired(),
                                    length(max=30)])
    last_name = StringField("Last Name:",
                        validators=[InputRequired(),
                                    length(max=30)])


class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField(
                        "Username:",
                        validators=[InputRequired(),
                                    length(max=20)])
    password = PasswordField("Password:",
                            validators=[InputRequired()])


class NoteForm(FlaskForm):
    """Form for creating a new note"""

    title = StringField(
                        "Title:",
                        validators=[InputRequired(),
                                    length(max=100)])
    content = StringField("Content:",
                            validators=[InputRequired()])

class NoteUpdateForm(FlaskForm):
    """Form for updating a note"""

    title = StringField(
                        "Title:",
                        validators=[InputRequired(),
                                    length(max=100)])
    content = StringField("Content:",
                            validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """empty Delete Form for CSRF protection"""
    #pass
    # or 
    #...


