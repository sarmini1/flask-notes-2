"""Seed file to make sample data for notes app db."""

from models import User, Note, db
from app import app


# Create all tables
db.drop_all()
db.create_all()

first_user = {"username":"spencer",
                "email":"name@email.com",
                  "pwd":"PW123",
                  "first_name":"spencer",
                  "last_name":"armini"}
second_user = {"username":"spencer2",
                "email":"namasdfe@email.com",
                  "pwd":"PW1234",
                  "first_name":"spencer",
                  "last_name":"armini"}
user = User.register(**first_user)
user2 = User.register(**second_user)

db.session.add(user)
db.session.add(user2)
db.session.commit()

first_note = Note(title="first_note",
                  content="a;slkdjf;laksdf",
                  owner=user.username)
second_note = Note(title="second_note",
                  content="a;slkdjf;laksdf",
                  owner=user2.username)

db.session.add(first_note)
db.session.add(second_note)
db.session.commit()
