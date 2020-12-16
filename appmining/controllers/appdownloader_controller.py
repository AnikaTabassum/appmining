# """
# Routes and views for the flask application.
# """
from datetime import datetime
from flask import render_template, redirect, request, jsonify, session
import json

from appmining import app
from appmining.services import *
@app.route('/')
@app.route('/apps')
def appsearch():
	print("try")
	appdownloader().whoamI()
	return render_template('appsearch/index.html')
