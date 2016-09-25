import boto
from boto.s3.key import Key
from werkzeug.utils import secure_filename
import hashlib
import os
import sendgrid
import re
import cgi
from yurl import URL
from titlecase import titlecase

def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True

def is_length_of_name_valid(name):
    if len(name) > 0 and len(name) < 76:
        return True
    return False

def is_length_of_password_valid(password):
    if len(password) > 5 and len(password) < 51:
        return True
    return False  