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
import json
import traceback
import os
import requests
from datetime import datetime

splash = Blueprint('splash', __name__, template_folder="templates")
access_token = os.environ['CS490_MESSENGER_TOKEN']

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@splash.route('/')
def index():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('splash.success'))
    email = request.args.get('defaultEmail')
    return render_template('home.html', email=email)

@splash.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/favicon'), 'favicon-96x96.png', mimetype='image/vnd.microsoft.icon')

@splash.route('/success', methods=['GET'])
def success():
    if current_user is not None and current_user.is_authenticated():
        return render_template('success.html')
    return redirect(url_for('splash.index'))

@splash.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'GET':
        print "here"
        token = request.args.get('hub.verify_token')
        print token
        print "success"
        return request.args.get('hub.challenge')
        return render_template('success.html')
    try:
        data = json.loads(request.data)
        print data
        text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
        print text
        sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
        if User.query.filter(User.facebook_id == sender).first() is None:
            if User.query.filter(User.facebook_code == text).first() is None:
                payload = {'recipient': {'id': sender}, 'message': {'text': "We don't recognize this account."}} # We're going to send this back
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=payload) # Lets send it
                print "wtf"
                return 'wtf'
            else:
                payload = {'recipient': {'id': sender}, 'message': {'text': "Your account has been verified!"}} # We're going to send this back
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=payload) # Lets send it
                user = User.query.filter(User.facebook_code == text).first()
                user.facebook_id = sender
                print user.facebook_id
                db.commit()
                return 'committed'
        else:
            user = User.query.filter(User.facebook_id == sender).first()
            if ((datetime.now() - user.last_login_attempt).seconds > 86400):
                payload = {'recipient': {'id': sender}, 'message': {'text': "Success!"}} # We're going to send this back
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=payload) # Lets send it
                user.last_login_attempt = None
                db.commit()
                print "success"
                login_user(user)
                return 'success'

    except Exception as e:
        print traceback.format_exc() # something went wrong

# def messaging_events(payload):
#     data = json.loads(payload)
#     messaging_events = data["entry"][0]["messaging"]
#     for event in messaging_events:
#         if "message" in event and "text" in event["message"]:
#             yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
#         else:
#             yield event["sender"]["id"], "I can't echo this"

# def send_message(token, recipient, text):
#     r = requests.post("https://graph.facebook.com/v2.6/me/messages",
#         params={"access_token": token},
#         data=json.dumps({
#         "recipient": {"id": recipient},
#         "message": {"text": text.decode('unicode_escape')}
#         }),
#         headers={'Content-type': 'application/json'})
#     if r.status_code != requests.codes.ok:
#         print r.text


@splash.route('/error', methods=['GET'])
def error():
    return render_template('error.html')

@splash.route('/confirm_facebook', methods=['GET'])
def confirm_facebook():
    token = request.args.get('token')
    if current_user is not None and token is not None:
        return render_template('confirm_facebook.html')
    return redirect(url_for('splash.index'))

@splash.route('/submitted', methods=['GET'])
def submitted():
    status = request.args.get('code')
    user = None
    if status == "1":
        email = request.args.get('email')
        return render_template('submitted.html', email=email)
    elif status == "2":
        confirmation_code = request.args.get('confirmationCode')
        print confirmation_code
        matched = User.query.filter(User.confirmation_code==confirmation_code)
        if matched.count() == 0:
            return redirect(url_for('splash.index'))
        user = matched.first()
        if user.email_confirmation_status == 1:
            return redirect(url_for('splash.index'))
        user.email_confirmation_status = 1
        rand = uuid.uuid4().hex
        user.facebook_code = rand
        db.session.commit()
        # login_user(user)
        return redirect(url_for('splash.confirm_facebook', token=rand))
    return redirect(url_for('splash.index'))

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
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    if not is_email_address_valid(email):
        flash('Not a valid email address')
        return redirect(url_for('splash.error', code="3"))
    email = email.encode('utf8')

    a = User(email=email, firstname=firstname, lastname=lastname)
    password = request.form['password']
    if not is_length_of_password_valid(password) or not password == request.form['cpassword']:
        flash('Your passwords didn\'t match!')
        return redirect(url_for('splash.error', code="3"))
    a.hash_password(password)
    uid = uuid.uuid4().hex
    while (User.query.filter(User.confirmation_code==uid).count() > 0):
        uid = uuid.uuid4().hex
    a.confirmation_code = uid
    db.session.add(a)
    db.session.commit()
    sendConfirmationEmail(a)
    login_user(a)

    return redirect(url_for('splash.submitted', code="1", email=a.email))


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
        return redirect(url_for('splash.error'))
    if user.email_confirmation_status == 0:
        flash('Please confirm your account first.')
        return redirect(url_for('splash.error'))
    if user.facebook_confirmation_status == 0:
        return redirect(url_for('splash.confirm_facebook', token=user.facebook_code))
    if ((datetime.now() - user.last_successful_login).seconds > 3600):
        user.last_login_attempt = datetime.now()
        redirect(url_for('splash.index'))
    redirect(url_for('splash.success'))

    # login_user(user)
    

@splash.route("/logout", methods=['GET'])
@login_required
def logout():
    email = current_user.email
    logout_user()
    return redirect(url_for('splash.index', defaultEmail=email))

@splash.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    if request.method == 'GET':
        return render_template('password.html')
    user = current_user
    code = 0
    password = request.form['opassword']
    if not user.verify_password(password):
        code = 3
    password = request.form['password']
    if not password == request.form['cpassword']:
        code = 3
    if not is_length_of_password_valid(password):
        code = 3
    if code == 0:
        user.hash_password(password)
        db.session.commit()
    return redirect(url_for('splash.index', code=code))

@splash.route('/forgot-password', methods=['POST'])
def forgotPassword():
    email = request.form['email'].lower()
    user = User.query.filter(User.email == email).first()
    if user is None:
        return jsonify({'response': 1})
    uid = uuid.uuid4().hex
    while (User.query.filter(User.password_reset_token == uid).count() > 0):
        uid = uuid.uuid4().hex
    user.password_reset_token = uid
    status = sendPasswordResetEmail(user)
    db.session.commit()
    return jsonify({'response': status})

@splash.route('/reset-password', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'GET':
        token = request.args.get('token')
        if token is None:
            return redirect(url_for('splash.login'))
        user = User.query.filter(User.password_reset_token == token).first()
        if not user:
            return redirect(url_for('splash.login'))
        return render_template('reset-password.html', token=token)
    token = request.form['token']
    if token is None:
        return render_template('update/password_failure.html', unauthenticated=True)
    password = request.form['password']
    cpassword = request.form['cpassword']
    user = User.query.filter(User.password_reset_token == token).first()
    if not user:
        return render_template('update/password_failure.html', unauthenticated=True)
    if not is_length_of_password_valid(password) or not password == cpassword:
        return render_template('dashboard/update/password_failure.html', unauthenticated=True)
    user.hash_password(password)
    user.password_reset_timestamp = None
    user.password_reset_token = None
    db.session.commit()
    logout_user()
    login_user(user)
    return redirect(url_for('splash.index'))


