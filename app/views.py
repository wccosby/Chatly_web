from flask import Flask, jsonify, request, render_template, flash, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from app import app
# from .forms import LoginForm
# from app import User, Story, db, Question, n2nModel
import os

from app.database import db_session
from app.models import User, Story, n2nModel

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
            session['userid'] = user.id
            session['name'] = user.name
            return render_template('story.html', userid=user.id, name=user.name)
            # return redirect(url_for("story", userid=user.id, name=user.name))
        else: # user doesnt exist so lets add them to the database
            user = User(name=result['first_name'], email=result['email'], password=result['password'])
            db_session.add(user)
            db_session.commit()
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
        story_file = request.files.get('story_file')
        faq_file = request.files.get('faq_file')
        # read this file to the sql database
        story_text = unicode(story_file.read(), "utf-8")
        faq_text = unicode(faq_file.read(), "utf-8")
        story = Story(story_text=story_text, user_id=session['userid'], faq=faq_text)
        db_session.add(story)
        db_session.commit()
        # get a reference to the story id to pass into the FAQ function
        story = Story.query.filter_by(user_id=session['userid']).first()
        session['storyid'] = story.id
        # redirect to processing page
        # return render_template('processing_data.html')
        return redirect(url_for('processing_data'))


@app.route('/processing')
def processing_data():
    '''
    needs to associate this specific model with the story id and the user id

    '''
    render_template('processing_data.html')

@app.route('/questions_page')
def questions_page():
    return render_template('questions_page.html')

@app.route("/home")
def home():
    return render_template('home.html')


#TODO implement the api in the route below (right now there is an example right below it that does the stuff)
@app.rout("/model_pred", methods=['POST'])
def model_Prediction():
    '''
    Posting sends up an access code, and a question, then gets an answer as a return
    '''



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
