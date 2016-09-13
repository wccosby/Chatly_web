from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from app import app
from .forms import LoginForm
from .models import User, db

from flask_bcrypt import Bcrypt
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt()

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login"))


@app.route('/login', methods=["GET","POST"])
def login():
    """
    For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    print db
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrtpt.check_password_has(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("index"))
    return render_template("login.html",form=form)

# Homepage
@app.route("/")
@app.route("/index")
@login_required
def index():
    """
    Homepage: serve our visualization page, index.html
    """
    logged_in=False
    return render_template('index.html',
                            logged_in=logged_in)

@app.route("/home")
def home():
    return render_template('home.html')


# @app.route('/login', methods=['GET','POST'])
# def login():
#     return render_template('login.html')

# # Get an example and return it's score from the predictor model
# @app.route("/score/", methods=["POST"])
# def score():
#     """
#     When A POST request with json data is made to this uri,
#     Read the example from the json, predict probability and
#     send it with a response
#     """
#     # # Get decision score for our example that came with the request
#     # data = request.json
#     # x = np.matrix(data["example"])
#     # score = PREDICTOR.predict_proba(x)
#     # # Put the result in a nice dict so we can send it as json
#     # results = {"score": score[0,1]}
#     # return jsonify(results)
#     raise Exception("Implement this!")

#--------- RUN WEB APP SERVER ------------#
