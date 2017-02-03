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

    # if user found, check if password matches
    if password == user_check.password:
        session['user_id'] = user_check.user_id
        flash("Logged in successfully")
        route = "/userpage/" + str(user_check.user_id)
        return redirect(route)
    else:
        flash("Wrong password!")
        return render_template("login_form.html")


@app.route('/logout')
def logout():
    del session['user_id']
    flash("Logged out successfully")
    return redirect("/")


@app.route('/register', methods=["GET"])
def display_register_form():

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def process_register_form():
    email = request.form.get("email")
    password = request.form.get("password")

    #Check if user already exists, if not create user and add to table
    try:
        user_check = User.query.filter_by(email=email).one()
        flash("Email already registered!")
        return render_template("register_form.html")
    except NoResultFound:
        user = User(email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.user_id
        flash("You are registered & logged in.")
        return render_template("homepage.html")

@app.route('/userpage/<user_id>')
def display_user(user_id):
    # user_id = request.args.get('user_id')

    user_info = User.query.get(user_id)

    user_ratings_objects = user_info.ratings

    return render_template("user_details.html", user_info=user_info,
                            user_ratings_objects=user_ratings_objects)


@app.route('/movielist/')
def display_movies():
    movies = Movie.query.all() #order....
    return render_template("movie_list.html", movies=movies)


@app.route('/moviedetails/<movie_id>')
def display_movie(movie_id):

    movie_info = Movie.query.get(movie_id)

    movie_ratings_objects = movie_info.ratings

    return render_template("movie_details.html",
                            movie_info=movie_info,
                            movie_ratings_objects=movie_ratings_objects)


@app.route('/rating', methods=["POST"])
def process_rating():
    user_id = session["user_id"]
    movie_id = int(request.form.get("movie_id"))
    score = int(request.form.get("score"))

    print user_id
    print movie_id
    print score

    try:
        user_movie_check = Rating.query.filter_by(user_id=user_id,
                                                  movie_id=movie_id).one()
        user_movie_check.score = score
        db.session.commit()

        flash("Your rating has been updated.")
        return redirect('/moviedetails/%s' % (movie_id))

    except NoResultFound:
        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)
        db.session.add(rating)
        db.session.commit()

        flash("Your rating has been submitted")
        return redirect('/moviedetails/%s' % (movie_id))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure tuser_emplates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
