from main import db
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(30))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow())

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '#%d: First Name: %s, Last Name: %s, Email: %s, Registered On: %s, Password: %s' % (self.id, self.firstname, self.lastname, self.email, self.registered_on.strftime('%m/%d/%Y at %H:%M:%S GMT'), self.password)


class Attendee(db.Model):
    __tablename__ = 'attendees'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    password = db.Column(db.String(200))
    email = db.Column(db.String(80), unique=True, index=True)
    status = db.Column(db.String(20), default="pending")
    graduation_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
    
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '#%d: First Name: %s, Last Name: %s, Email: %s, Status: %s, Graduation: %s, Major: %s, School: %s, Linkedin: %s, Github: %s, Personal: %s, Resume: %s, Registered: %s, Confirmation Code: %s, Confirmation Status: %d, Password Reset Token: %s' % (self.id, self.firstname, self.lastname, self.email, self.status, self.graduation_year, self.major, self.school, self.linkedin_url, self.github_url, self.personal_url, self.resume_url, self.registered_on.strftime('%m/%d/%Y at %H:%M:%S GMT'), self.confirmation_code, self.confirmation_status, self.password_reset_token)
