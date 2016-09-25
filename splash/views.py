from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for, flash)
from flask_login import login_user, logout_user, current_user, login_required
from main import app, login_manager
from functools import wraps
from user.models import Attendee
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
    return Attendee.query.get(int(id))


@app.errorhandler(413)
def file_too_big(e):
    return redirect(url_for('splash.index', code="3"))

@splash.route('/')
def index():
    firstLoading = not request.cookies.get('c209a57ae54980562bf78bd802b06b97')
    return render_template('home.html', firstLoading=firstLoading)

@splash.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/favicon'), 'favicon-96x96.png', mimetype='image/vnd.microsoft.icon')

@splash.route('/submitted', methods=['GET'])
def submitted():
    status = request.args.get('code')
    if status == None:
        return redirect(url_for('splash.index'))
    elif status == "2":
        confirmation_code = request.args.get('confirmationCode')
        print confirmation_code
        matched = Attendee.query.filter(Attendee.confirmation_code==confirmation_code)
        if matched.count() == 0:
            return redirect(url_for('splash.index'))
        attendee = matched.first()
        if attendee.confirmation_status == 1:
            return redirect(url_for('splash.index'))
        attendee.confirmation_status = 1
        db.session.commit()
        return render_template('statuses/confirmed.html', firstName=attendee.firstname)
    else:
        ref = request.referrer
        if ref == None:
            return redirect(url_for('splash.index'))
        ref = urlparse(ref)
        if (ref.netloc not in ['localhost:5000', 'yhack.org', 'www.yhack.org', 'www.yhack-2016-prod.herokuapp.com', 'yhack-2016-prod.herokuapp.com', 'www.yhack-2016-staging.herokuapp.com', 'yhack-2016-staging.herokuapp.com']):
            return redirect(url_for('splash.index'))
        if (ref.path not in ['/apply']):
            return redirect(url_for('splash.index'))

        if status == "0":
            return render_template('statuses/completed.html')
        elif status == "1":
            email = request.args.get('email')
            return render_template('statuses/submitted.html', email=email)
        elif status == "3":
            return render_template('statuses/rejected.html')
    return redirect(url_for('splash.index'))

@splash.route('/resend-confirmation', methods=['GET'])
def resendEmail():
    ref = request.referrer
    if ref == None:
        return redirect(url_for('splash.index'))
    ref = urlparse(ref)
    if (ref.netloc not in ['localhost:5000', 'yhack.org', 'www.yhack.org', 'www.yhack-2016-prod.herokuapp.com', 'yhack-2016-prod.herokuapp.com', 'www.yhack-2016-staging.herokuapp.com', 'yhack-2016-staging.herokuapp.com']):
        return redirect(url_for('splash.index'))
    if (ref.path not in ['/submitted']):
        return redirect(url_for('splash.index'))
    email = request.args.get('email')
    if email is None:
        return redirect(url_for('splash.index'))
    user = Attendee.query.filter(Attendee.email==email).first()
    if user is None:
        return redirect(url_for('splash.index'))
    if user.confirmation_status == 1:
        return jsonify({'message':'It appears your account is already confirmed!'})
    if user.confirmation_emails_sent > 1:
        return jsonify({'message':'Your confirmation has been resent! If you still do not receive an email, please contact <a href="mailto:team@yhack.org">team@yhack.org</a>.'})
    sendConfirmationEmail(user)
    user.confirmation_emails_sent = user.confirmation_emails_sent + 1
    db.session.commit()
    return jsonify({'message':'Confirmation resent!'})

@splash.route('/apply', methods=['GET', 'POST'])
def apply():
    #######################################
    ####### Close 2016 Applications #######
    #######################################
    # return redirect(url_for('splash.index'))
    #######################################

    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('dashboard.index'))

    if request.method == 'GET':
        return render_template('apply.html')

    # for debugging
    requestDict = request.values
    requestDict = dict(zip(requestDict, map(lambda x: requestDict.get(x), requestDict)))
    del requestDict['password']
    del requestDict['cpassword']
    print requestDict

    if Attendee.query.filter(Attendee.email == request.form['email'].strip().lower()).count() == 1:
        return redirect(url_for('splash.submitted', code="0"))

    school = request.form['school']
    if school == "other":
        school = request.form['school-other-field']
    if not is_length_of_school_valid(school):
        print "got here 2"
        return redirect(url_for('splash.submitted', code="3"))
    school = school.encode('utf8')

    firstname = request.form['firstname'].strip().title()
    if not is_length_of_name_valid(firstname):
        print "got here 3"
        return redirect(url_for('splash.submitted', code="3"))
    firstname = firstname.encode('utf8')

    lastname = request.form['lastname'].strip().title()
    if not is_length_of_name_valid(lastname):
        print "got here 4"
        return redirect(url_for('splash.submitted', code="3"))
    lastname = lastname.encode('utf8')

    email = request.form['email'].strip().lower()
    if not is_email_address_valid(email):
        print "got here 5"
        return redirect(url_for('splash.submitted', code="3"))
    email = email.encode('utf8')

    graduation_year = request.form['graduation_year']
    if graduation_year not in ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']:
        print "got here 6"
        return redirect(url_for('splash.submitted', code="3"))
    graduation_year = graduation_year.encode('utf8')

    gender = request.form['gender']
    if gender not in ['male', 'female', 'nonbinary', 'other', 'pnd']:
        print "got here gender"
        return redirect(url_for('splash.submitted', code="3"))
    gender = gender.encode('utf8')

    race = request.form['race']
    if race not in ['white', 'hispanic', 'black', 'nativeamerican', 'asian', 'other', 'pnd']:
        print "got here race"
        return redirect(url_for('splash.submitted', code="3"))
    race = race.encode('utf8')

    major = request.form['major']
    if not is_length_of_major_valid(major):
        print "got here 7"
        return redirect(url_for('splash.submitted', code="3"))
    major = major.encode('utf8')

    previous_hackathons = request.form['previous_hackathons']
    if previous_hackathons not in ['0', '1', '2', '3', '4', '5']:
        print "got here previous hackathons"
        return redirect(url_for('splash.submitted', code="3"))
    previous_hackathons = int(previous_hackathons)

    linkedin_url = request.form['linkedin_url'].encode('utf8')
    if linkedin_url:
        if not is_url_valid(linkedin_url):
            print "got here 8"
            return redirect(url_for('splash.submitted', code="3"))

    github_url = request.form['github_url'].encode('utf8')
    if github_url:
        if not is_url_valid(github_url):
            print "got here 9"
            return redirect(url_for('splash.submitted', code="3"))

    personal_url = request.form['personal_url'].encode('utf8')
    if personal_url:
        if not is_url_valid(personal_url):
            print "got here 10"
            return redirect(url_for('splash.submitted', code="3"))

    projects_and_awards = request.form['projects_and_awards'].strip()
    if projects_and_awards:
        if not is_length_of_projects_and_awards_valid(projects_and_awards):
            print "got here 11"
            return redirect(url_for('splash.submitted', code="3"))
    projects_and_awards = projects_and_awards.encode('utf8')

    file = request.files['resume']
    if file:
        if getFileSize(file) < (10*1024*1024):
            resume_url = resume_upload(file)
        else:
            resume_url = None
            print "Ignoring resume of %s - too big." %(request.form['email'])
    else:
        resume_url = None

    a = Attendee(firstname=firstname, lastname=lastname, email=email, graduation_year=graduation_year, gender=gender, race=race, major=major, school=school, previous_hackathons=previous_hackathons, linkedin_url=linkedin_url, github_url=github_url, personal_url=personal_url, resume_url=resume_url, projects_and_awards=projects_and_awards)
    password = request.form['password']
    if not is_length_of_password_valid(password) or not password == request.form['cpassword']:
        print "got here 12"
        return redirect(url_for('splash.submitted', code="3"))
    a.hash_password(password)
    uid = uuid.uuid4().hex
    while (Attendee.query.filter(Attendee.confirmation_code==uid).count() > 0):
        uid = uuid.uuid4().hex
    a.confirmation_code = uid
    db.session.add(a)
    db.session.commit()
    sendConfirmationEmail(a)
    return redirect(url_for('splash.submitted', code="1", email=a.email))


@splash.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('dashboard.index'))
    if request.method == 'GET':
        email = request.args.get('defaultEmail')
        return render_template('login.html', email=email)
    email = request.form['email'].lower()
    password = request.form['password']
    attendee = Attendee.query.filter(Attendee.email == email).first()
    if attendee is None:
        flash('No application with that email exists, try again!')
        return redirect(url_for('splash.login'))
    if attendee.verify_password(password) is False:
        flash('That email/password combination does not exist, try again!')
        return redirect(url_for('splash.login', defaultEmail=email))
    if attendee.confirmation_status == 0:
        flash('Please confirm your account first.')
        return redirect(url_for('splash.login'))
    login_user(attendee)
    return redirect(url_for('dashboard.index'))

@splash.route('/forgot-password', methods=['POST'])
def forgotPassword():
    email = request.form['email'].lower()
    attendee = Attendee.query.filter(Attendee.email == email).first()
    if attendee is None:
        return jsonify({'response': 1})
    uid = uuid.uuid4().hex
    while (Attendee.query.filter(Attendee.password_reset_token == uid).count() > 0):
        uid = uuid.uuid4().hex
    attendee.password_reset_token = uid
    attendee.password_reset_timestamp = datetime.utcnow()
    status = sendPasswordResetEmail(attendee)
    db.session.commit()
    return jsonify({'response': status})

@splash.route('/reset-password', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'GET':
        token = request.args.get('token')
        if token is None:
            return redirect(url_for('splash.login'))
        attendee = Attendee.query.filter(Attendee.password_reset_token == token).first()
        if not attendee:
            return redirect(url_for('splash.login'))
        return render_template('reset-password.html', token=token)
    token = request.form['token']
    if token is None:
        return render_template('update/password_failure.html', unauthenticated=True)
    password = request.form['password']
    cpassword = request.form['cpassword']
    attendee = Attendee.query.filter(Attendee.password_reset_token == token).first()
    if not attendee:
        return render_template('update/password_failure.html', unauthenticated=True)
    if not is_length_of_password_valid(password) or not password == cpassword:
        return render_template('dashboard/update/password_failure.html', unauthenticated=True)
    if ((datetime.now() - attendee.password_reset_timestamp).seconds > 86400):
        attendee.password_reset_timestamp = None
        attendee.password_reset_token = None
        db.session.commit()
        return render_template('update/password_failure.html', unauthenticated=True, oldToken=True)
    attendee.hash_password(password)
    attendee.password_reset_timestamp = None
    attendee.password_reset_token = None
    db.session.commit()
    logout_user()
    login_user(attendee)
    return redirect(url_for('splash.login', defaultEmail=attendee.email))
    

@splash.route("/logout", methods=['GET'])
@login_required
def logout():
    email = current_user.email
    logout_user()
    return redirect(url_for('splash.login', defaultEmail=email))

@splash.route("/volunteer", methods=['GET'])
def volunteer():
    return redirect("https://www.facebook.com/events/928766723861583/", code=302)

@splash.route("/cs50", methods=['GET'])
def cs50():
    return redirect(url_for('splash.apply'))

