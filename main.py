"""
YHack Admin 2015 app setup
"""


from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from flask_login import LoginManager

# Set up app with debugging
app = Flask(__name__)
app.debug = True

# Login manager for authentication.  If not authenticated, route to login page
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'splash.login'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['CS490_DATABASE_URL']
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

db = SQLAlchemy(app)

# for flask-login -- secret key needed to use sessions
app.secret_key = os.environ['USER_AUTH_SECRET_KEY']
