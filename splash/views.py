from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for, flash)
from flask_login import login_user, logout_user, current_user, login_required
from main import app, login_manager
from functools import wraps
from user.models import User
from main import db
import pdb
from user import *
from flask import Markup
import uuid
from urlparse import urlparse
from splash import *
import cgi
import os
from datetime import datetime

splash = Blueprint('splash', __name__, template_folder="templates")


@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@splash.route('/')
def index():
    return render_template('home.html')

@splash.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/favicon'), 'favicon-96x96.png', mimetype='image/vnd.microsoft.icon')

@splash.route('/success', methods=['GET'])
def success():
    if current_user is not None and current_user.is_authenticated():
        return render_template('success.html')
    return redirect(url_for('splash.index'))

@splash.route('/authenticate', methods=['GET', 'POST'])
@login_required
def authenticate():
    if request.method == 'GET':
        return render_template('success.html')

@splash.route('/error', methods=['GET'])
def error():
    return render_template('error.html')

@splash.route('/create', methods=['POST'])
def create():
    requestDict = request.values
    requestDict = dict(zip(requestDict, map(lambda x: requestDict.get(x), requestDict)))
    del requestDict['password']
    del requestDict['cpassword']
    print requestDict

    if User.query.filter(User.email == request.form['email'].strip().lower()).count() == 1:
        flash('A user with that email has already created an account')
        return redirect(url_for('splash.error', code="0"))

    email = request.form['email'].strip().lower()
    if not is_email_address_valid(email):
        flash('Not a valid email address')
        return redirect(url_for('splash.error', code="3"))
    email = email.encode('utf8')

    a = User(email=email)
    password = request.form['password']
    if not is_length_of_password_valid(password) or not password == request.form['cpassword']:
        flash('Your passwords didn\'t match!')
        return redirect(url_for('splash.error', code="3"))
    a.hash_password(password)
    uid = uuid.uuid4().hex
    db.session.add(a)
    db.session.commit()
    login_user(a)

    return redirect(url_for('splash.success', code="1", email=a.email))


@splash.route('/login', methods=['POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('splash.success'))
    email = request.form['email'].lower()
    password = request.form['password']
    user = User.query.filter(User.email == email).first()
    if user is None:
        flash('No user with that email exists, try again!')
        return redirect(url_for('splash.error'))
    if user.verify_password(password) is False:
        flash('That email/password combination does not exist, try again!')
        return redirect(url_for('splash.error', defaultEmail=email))
    login_user(user)
    return redirect(url_for('splash.success'))
    

@splash.route("/logout", methods=['GET'])
@login_required
def logout():
    email = current_user.email
    logout_user()
    return redirect(url_for('splash.index', defaultEmail=email))


