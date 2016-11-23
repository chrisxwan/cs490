from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for, flash)
from flask_login import login_user, logout_user, current_user, login_required
from main import app, login_manager
from functools import wraps
from user.models import User
from service.models import Service
from service_user.models import ServiceUser
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
from Crypto.PublicKey import RSA
import base64


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
    return render_template('home.html')

@splash.route('/configure_sso', methods=['GET', 'POST'])
def configure_sso():
    if request.method == 'GET':
        return render_template('configure_sso.html')
    name = request.form.get('name').lower()
    entrypoint = request.form.get('entrypoint-url').lower()
    acs = request.form.get('acs-url').lower()
    key = request.files.get('key')
    if key is None:
        flash('Please upload RSA key')
        return redirect(url_for('splash.error'))
    public_key = RSA.importKey(key.read()).exportKey()
    print(public_key)
    s = Service(name=name, entrypoint=entrypoint, acs=acs, public_key=public_key)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('splash.index'))

@splash.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/favicon'), 'favicon-96x96.png', mimetype='image/vnd.microsoft.icon')

@splash.route('/success', methods=['GET'])
def success():
    if current_user is not None and current_user.is_authenticated():
        if current_user.email_confirmation_status != 1:
            return redirect(url_for('splash.submitted', code = 1, email = current_user.email))
        elif current_user.facebook_confirmation_status != 1:
            return redirect(url_for('splash.confirm_facebook', token = current_user.facebook_code, email = current_user.email, ))
        return render_template('success.html')
    return redirect(url_for('splash.index'))

@splash.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        print token
        return request.args.get('hub.challenge')
    try:
        data = json.loads(request.data)
        print data
        if 'message' not in data['entry'][0]['messaging'][0]:
            print "wtf???"
            return '0'
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
                user.facebook_confirmation_status = 1
                user.facebook_id = sender
                user.last_login_attempt = None
                user.last_successful_login = datetime.now()
                print user.facebook_id
                db.session.commit()
                login_user(user)
                return 'committed'
        else:
            user = User.query.filter(User.facebook_id == sender).first()
            if ((datetime.now() - user.last_login_attempt).seconds < 300):
                payload = {'recipient': {'id': sender}, 'message': {'text': "Success!"}} # We're going to send this back
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=payload) # Lets send it
                user.last_login_attempt = None
                user.last_successful_login = datetime.now()
                db.session.commit()
                print "success"
                login_user(user)
                return "success"
            else:
                payload = {'recipient': {'id': sender}, 'message': {'text': "Failed to authenticate in time! Login again."}} # We're going to send this back
                r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=payload) # Lets send it
                return "failed to login in time"

    except Exception as e:
        print traceback.format_exc() # something went wrong

@splash.route('/error', methods=['GET'])
def error():
    return render_template('error.html')

@splash.route('/confirm_facebook', methods=['GET'])
def confirm_facebook():
    token = request.args.get('token')
    email = request.args.get('email')
    service_email = request.args.get('service_email')
    service = request.args.get('service')
    service_acs = request.args.get('service_acs')
    if email is not None:
        user = User.query.filter(User.email == email).first()
        if user.facebook_code == token:
            if service is not None and service_email is not None and service_acs is not None:
                s = Service.query.filter(Service.name == service).first()
                public_key = s.public_key
                public_key = RSA.importKey(public_key)
                service_email = public_key.encrypt(str(service_email), 32)
                service_email = base64.b64encode(service_email[0])
            return render_template('confirm_facebook.html', facebook_code = user.facebook_code, email = email, service_email=service_email, service_acs=service_acs)
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
        return redirect(url_for('splash.confirm_facebook', token=rand))
    return redirect(url_for('splash.index'))

@splash.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('register.html')
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

@splash.route('/check_db', methods=['POST'])
def check_db():
    email = request.args.get('email')
    user = User.query.filter(User.email == email).first()
    if user.last_successful_login is not None:
        login_user(user)
        return "1"
    return "0"

@splash.route('/authenticate_facebook', methods=['GET'])
def authenticate_facebook():
    email = request.args.get('email')
    service_email = request.args.get('service_email')
    service = request.args.get('service')
    service_acs = request.args.get('service_acs')
    return render_template('authenticate_facebook.html', email = email, service=service, service_email = service_email, service_acs=service_acs)

@splash.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        service = request.args.get('service')
        service_email = request.args.get('service_email')
        if service is not None and service_email is not None:
            s = Service.query.filter(Service.name == service).first()
            if s is None:
                return redirect(url_for('splash.index'))
        return render_template('login.html', service=service, service_email=service_email)
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('splash.success'))
    email = request.form['email'].lower()
    password = request.form['password']
    user = User.query.filter(User.email == email).first()
    service = request.form.get('service').lower()
    service_email = request.form.get('service_email').lower()
    if user is None:
        flash('No user with that email exists, try again!')
        return redirect(url_for('splash.error'))
    if user.verify_password(password) is False:
        flash('That email/password combination does not exist, try again!')
        return redirect(url_for('splash.error'))
    if user.email_confirmation_status == 0:
        flash('Please confirm your account first.')
        return redirect(url_for('splash.error'))
    service_acs=None
    if service != 'none' and service_email != 'none':
        s = Service.query.filter(Service.name == service).first()
        if s is None:
            flash('Wrong service')
            return redirect(url_for('splash.error'))
        service_acs = s.acs
        su = ServiceUser.query.filter(ServiceUser.service == service).filter(ServiceUser.service_email == service_email).first()
        if su is None:
            print "here1"
            su = ServiceUser(service_email=service_email, service=service, internal_user=email)
            db.session.add(su)
            db.session.commit()
        elif su.internal_user != email:
            flash('Wrong login')
            return redirect(url_for('splash.error'))
    if user.facebook_confirmation_status == 0:
        user.last_login_attempt = datetime.now()
        db.session.commit()
        return redirect(url_for('splash.confirm_facebook', email = user.email, token=user.facebook_code, service=service, service_email=service_email, service_acs=service_acs))
    if (user.last_successful_login is None or (datetime.now() - user.last_successful_login).seconds > 3600):
        user.last_login_attempt = datetime.now()
        db.session.commit()
        return redirect(url_for('splash.authenticate_facebook', email = user.email, service=service, service_email=service_email, service_acs=service_acs))
    login_user(user)
    return redirect(url_for('splash.success'))
    

@splash.route("/logout", methods=['GET'])
@login_required
def logout():
    current_user.last_successful_login = None
    db.session.commit()
    logout_user()
    return redirect(url_for('splash.index'))

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


