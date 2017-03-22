"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
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


@app.route("/register", methods=["GET"])
def register_form():

    return render_template("register_form.html")


@app.route("/register-process", methods=["POST"])
def register_process():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    if (User.query.filter_by(email=email).all()) == []:
        new_user = User(email=email, password=password, age=age,
                        zipcode=zipcode)

        db.session.add(new_user)
        db.session.commit()

    #TBD: create edge case handling in case user does exist


    return redirect("/")


@app.route("/login", methods=["GET"])
def login_form():

    return render_template("login.html")


@app.route("/login-process", methods=["POST"])
def login_process():
    email = request.form.get("email")
    password = request.form.get("password")
#TBD: create edge case handling in case user doesn't exist
    user_object = User.query.filter_by(email=email).one()
    db_password = user_object.password

    if db_password == password:
        session["user_id"] = user_object.user_id
        flash('You were successfully logged in')
        return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/logout", methods=["GET"])
def logout_process():
    del session["user_id"]
    flash('You were successfully logged out')
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
