from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegistrationForm
from project_secrets import API_SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = API_SECRET_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def redirect_from_root_route():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def process_registration():
    """If GET request, takes user to registration form
        If POST request, validates inputs from user and registers them to db
    """

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        new_user = User.register(
                            username=username,
                            pwd=pwd,
                            first_name=first_name,
                            last_name=last_name,
                            email=email)
        db.session.add(new_user)
        db.session.commit()

    else:
        return render_template("registration_form.html", form=form)

