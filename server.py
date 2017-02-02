"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_lists():
    """page displays list of users
    """
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/login', methods=["GET"])
def display_login_form():
    """show the login form for exisitng users
    """

    return render_template("login_form.html")


@app.route('/login-validation', methods=["POST"])
def process_login_form():
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user_check = User.query.filter_by(email=email).one()
    except NoResultFound: 
        flash("Email not found")
        return redirect("/login")

    # if user found, chekc if password matches
    if password == user_check.password:
        session['user_id'] = user_check.user_id
        flash("Logged in successfully")
        return render_template("homepage.html")
    else:
        flash("Wrong password!")
        return render_template("login_form.html")


@app.route('/register', methods=["GET"])
def display_register_form():

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def process_register_form():
    email = request.form.get("email")
    password = request.form.get("password")

# error msg === raise orm_exc.NoResultFound("No row was found for one()")
# sqlalchemy.orm.exc.NoResultFound: No row was found for one()


    # #Check if user already exists, if not create user and add to table
    # try:
    #     user_check = User.query.filter_by(email=email).one()
    # except NoResultFound:
    #     user = User(email=email,
    #                 password=password)
    #     db.session.add(user)
    #     db.session.commit()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
