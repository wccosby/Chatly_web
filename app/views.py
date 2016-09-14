from flask import Flask, jsonify, request, render_template, flash, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from app import app
# from .forms import LoginForm
from app import User, Story, db, Question, n2nModel
import os

@app.route('/'   )
@app.route('/login',methods=["GET","POST"])
def login():
    """
    For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    if request.method == "GET":
        return render_template("login.html")
    else:
        result=request.form
        print(result['email'])
        user = User.query.filter_by(email=result['email']).first() # because email is unique
        # check if user exists
        if user:
            print("USER EXISTS!!!")
            print user.id
            session['userid'] = user.id
            session['name'] = user.name
            return render_template('story.html', userid=user.id, name=user.name)
            # return redirect(url_for("story", userid=user.id, name=user.name))
        else: # user doesnt exist so lets add them to the database
            user = User(name=result['first_name'], email=result['email'], password=result['password'])
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=result['email']).first()
            session['userid'] = user.id
            session['name'] = user.name
            print("ADDED USER")
            return render_template('story.html', userid=user.id, name=user.name)
            # return redirect(url_for("story", userid=user.id, name=user.name))

# Homepage
@app.route("/story", methods=["GET","POST"])
def story():
    """
    Homepage:   , story.html
    """
    # print("FROM STORY: ",session['userid'])
    if request.method == 'GET':
        return render_template('story.html')
    else:
        file = request.files.get('file')
        # read this file to the sql database
        story = Story(story_text=file.read(), user_id=session['userid'])
        db.session.add(story)
        db.session.commit()
        # get a reference to the story id to pass into the FAQ function
        story = Story.query.filter_by(user_id=session['userid']).last()
        session['storyid'] = story.id
        return redirect(url_for('questions_page'))

@app.route('/questions_page')
def questions_page():
    return render_template('questions_page.html')

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
