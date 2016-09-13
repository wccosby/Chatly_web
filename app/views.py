from flask import Flask, jsonify, request, render_template, flash, redirect
#
# import tensorflow as tf
# import numpy as np
# import pandas as pd

#---------- MODEL IN MEMORY ----------------#

# Read the scientific data on breast cancer survival,
# Build a LogisticRegression predictor on it
# patients = pd.read_csv("haberman.data", header=None)
# patients.columns=['age','year','nodes','survived']
# patients=patients.replace(2,0)  # The value 2 means death in 5 years
#
# X = patients[['age','year','nodes']]
# Y = patients['survived']
# PREDICTOR = LogisticRegression().fit(X,Y)


#---------- URLS AND WEB PAGES -------------#

# Initialize the app
# app = Flask(__name__)
# from app import views

from app import app

# Homepage
@app.route("/")
@app.route("/index")
def index():
    """
    Homepage: serve our visualization page, index.html
    """
    logged_in=False
    return render_template('index.html',
                            logged_in=logged_in)


@app.route('/login', methods=['GET','POST'])
def login():


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
