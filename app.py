from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegistrationForm, LoginForm, NoteForm
from project_secrets import API_SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = API_SECRET_KEY

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

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

        if User.query.get(username) is None:

            new_user = User.register(
                username=username,
                pwd=pwd,
                first_name=first_name,
                last_name=last_name,
                email=email)
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.username

            return redirect(f'/users/{new_user.username}')
        
        else:
             flash(f"Username {username} is already taken.")
             return render_template("registration_form.html", form=form)

    else:
        return render_template("registration_form.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username=username, pwd=pwd)

        if user:
            session["user_id"] = user.username
            return redirect(f'/users/{user.username}')

        else:
            flash("Invalid credentials")
            return render_template("login_form.html", form=form)

    else:
        return render_template("login_form.html", form=form)


@app.route('/users/<username>')
def get_secret(username):
    """
    Return the text "You made it!" (don’t worry, we’ll get rid of this soon)
    """

    user = User.query.get(username)
    if username == session.get("user_id"):
        return render_template('user_info.html', user=user)
    else:
        return redirect('/')


@app.route('/logout')
def logout_user():
    """Logs a user out and redirects to root route"""
    session.pop("user_id", None)
    return redirect('/')


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """deletes a user and all of their notes,
    clears session data and redirects to root"""
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("user_id", None)
    return redirect('/')


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """
    If GET, displays a form to add a new note
    If POST, processes new note and redirects to user's info page
    """
    user = User.query.get_or_404(username)
    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_note = Note(title=title,
                        content=content,
                        owner=user.username)
        db.session.add(new_note)
        db.session.commit()
        return redirect(f"/users/{user.username}")
    else:
        if username == session.get("user_id"):
            return render_template("new_note_form.html", form=form)
