from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegistrationForm, LoginForm, NoteForm, NoteUpdateForm, DeleteForm
from project_secrets import API_SECRET_KEY

#try except statements
from sqlalchemy.exc import IntegrityError

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

        try:
        #if User.query.get(username) is None:
            new_user = User.register(
                username=username,
                pwd=pwd,
                first_name=first_name,
                last_name=last_name,
                email=email)
                
            db.session.commit()
            #session["username"] for consistency
            session["username"] = new_user.username

            return redirect(f'/users/{new_user.username}')
        
        except IntegrityError:
            #catch only IntegrityErrors
             flash(f"Username {username} is already taken.")
             return render_template("registration_form.html", form=form)

    else:
        return render_template("registration_form.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """
    Show a form that when submitted will authenticate & login a user. 
    This form should accept a username and a password.
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.authenticate(username=username, pwd=pwd)

        if not user:
            flash("Invalid credentials")
            return render_template("login_form.html", form=form)

        session["username"] = user.username
        return redirect(f'/users/{user.username}')

    else:
        return render_template("login_form.html", form=form)


@app.route('/users/<username>')
def show_user(username):
    """
    Show user page with list of notes by that user
    """

    if "username" not in session or username != session["username"]:
        flash("Unauthorized")
        return redirect('/')

    form = DeleteForm()
    # form with hidden tag 
    user = User.query.get(username)
    return render_template('user_info.html', user=user, form=form)        


@app.route('/logout')
def logout_user():
    """Logs a user out and redirects to root route"""
    session.pop("username")
    return redirect('/')


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """deletes a user and all of their notes,
    clears session data and redirects to root"""
    form = DeleteForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

    return redirect('/')


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """
    If GET, displays a form to add a new note
    If POST, processes new note and redirects to user's info page
    """
    #fail fast
    #redirect and flash first
    user = User.query.get_or_404(username)

    if "username" not in session or username != session["username"]:
        flash("You cannot add a note from this user")
        return redirect("/")
  
    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_note = Note(
            title=title,
            content=content,
            owner=user.username
            )
        db.session.add(new_note)
        db.session.commit()
        return redirect(f"/users/{user.username}")

    else:
        return render_template("new_note_form.html", form=form)

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """
    Show update note form with existing values,
    updates note changes in database
    """
    #fail fast

    note = Note.query.get_or_404(note_id)

    if "username" not in session or note.owner != session["username"]:
        flash("You cannot edit this note")
        return redirect("/")

    form = NoteUpdateForm(obj=note)
        
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()

        return redirect(f"/users/{note.owner}")
        
    else:
        return render_template(
            'note_update_form.html', 
            form=form
            )
        

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """
    Delete a note and redirect to user page if note belongs to 
    current user in session
    """
    if "username" not in session or note.owner != session["username"]:
        flash("You cannot delete this note")
        return redirect(f"/")

    form = DeleteForm()

    if form.validate_on_submit():
        session_user = session.get('username')
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return redirect(f'/users/{session_user}')
            