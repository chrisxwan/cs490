from main import db
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(30))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    confirmation_code = db.Column(db.String(50))
    confirmation_status = db.Column(db.Integer, default=0)
    password_reset_token = db.Column(db.String(50))

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
