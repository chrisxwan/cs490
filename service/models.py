from main import db
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True)
    entrypoint = db.Column(db.String(80), unique=True, index=True)
    acs = db.Column(db.String(80), unique=True, index=True)
    public_key = db.Column(db.String(500), unique=True)

    def __repr__(self):
        return '#%d: Name: %s, Entrypoint: %s, ACS: %s' % (self.id, self.name, self.entrypoint, self.acs)
