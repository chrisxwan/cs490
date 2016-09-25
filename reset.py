# import all models
from user.models import *

# recreate the database
db.drop_all()
db.create_all()

u = User(email="chrisxwan@gmail.com")
u.hash_password('helloworld')
db.session.add(u)
db.session.commit()