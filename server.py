"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                    session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


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
def user_list():
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def display_login_form():

    return render_template("register_form.html")


# @app.route('/register', methods=["POST"])
# def process_login_form():
#     email = request.form.get("email")
#     password = request.form.get("password")


#     user_check = User.query.filter_by(email=email).one()

#         add user

#     if user_check == []:
#         user = User(email=email,
#                     password=password)
#         db.session.add(user)
#         db.session.commit()
#     elif:
#         if password == user_check.password:
#         pass
#     #         # login
#     # else:
#         # passowrd does not match - back to form


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
