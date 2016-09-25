# importa all models
from user.models import *

# recreate the database
db.drop_all()
db.create_all()

a = Attendee(firstname="Jason", lastname="Brooks", email="jason.brooks@yale.edu", status="confirmed", confirmation_status=1)
a.hash_password('helloworld')
db.session.add(a)
db.session.commit()