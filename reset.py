# import all models
from user.models import *
from service.models import *
from service_user.models import *
import uuid

# recreate the database
db.drop_all()
db.create_all()


rand = uuid.uuid4().hex
u = User(email="chrisxwan@gmail.com", firstname="Christopher", lastname="Wan", email_confirmation_status=1, facebook_confirmation_status = 0, facebook_code=rand)
u.hash_password('helloworld')
db.session.add(u)
db.session.commit()