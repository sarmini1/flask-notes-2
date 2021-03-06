"""Models for Notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

# User class should include:
# tablename equal to "users"
# username, primary key, string (20)
# password, nullable is false, no char limit, can set as text
# email, nullable is false, unique, string (50)
# first_name, nullable is false, string(30)
# last_name, nullable is false, string(30)


class User(db.Model):
    """create a User"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                        primary_key=True)
    password = db.Column(db.Text,
                        nullable=False)
    email = db.Column(db.String(50),
                        unique=True,
                        nullable=False)
    first_name = db.Column(db.String(30),
                            nullable=False)
    last_name = db.Column(db.String(30),
                            nullable=False)

    notes = db.relationship('Note',
                            cascade="all,delete",
                            backref='notes')
                            # dont cascade very consequential

    def __repr__(self):
        return f'<User {self.username} {self.first_name} {self.last_name} >'

    @classmethod
    def register(cls, username, pwd, first_name, last_name, email):
        """Register user with hash password and return user"""

        hashed_password = bcrypt.generate_password_hash(pwd).decode('utf8')

        new_user = cls(
            username=username,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            email=email)

        db.session.add(new_user)
        

    @classmethod
    def authenticate(cls, username, pwd):
        """
        Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

# Note model should have:
# tablename of notes
# id, primary key, autoincrementing int
# title, string with limit of 100
# content, nullable is false, text type
# owner, foreign key referencing user.username


class Note(db.Model):
    """Create a note."""

    __tablename__ = "notes"

    id = db.Column(
                    db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(100),
                        nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    owner = db.Column(db.String(20),
                    db.ForeignKey("users.username"),
                    nullable=False)

    def __repr__(self):
        return f'<Note {self.id} {self.owner} {self.title} >'
