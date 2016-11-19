from main import db
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
from user.models import *
from service.models import *

class ServiceUser(db.Model):
    __tablename__ = 'service_users'
    id = db.Column(db.Integer, primary_key=True)
    service_email = db.Column(db.String(80), unique=True, index=True)
    internal_user = db.Column(db.String(80), db.ForeignKey('users.email'))
    internal_user_rel = db.relationship('User', foreign_keys=[internal_user], uselist=False)
    service = db.Column(db.String(80), db.ForeignKey('services.name'))
    service_rel = db.relationship('Service', foreign_keys=[service], uselist=False)

    def __repr__(self):
        return '#%d: Email: %s, Service: %s' % (self.id, self.email, self.service)
