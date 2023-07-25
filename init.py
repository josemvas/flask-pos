from pos import app
from pos.models import *
from config import Config
from getpass import getpass

password = getpass('Administrator password: ')
password2 = getpass('Confirm administrator password: ')
if password != password2:
    print('Passwords do not match!')
    raise SystemExit

user = User()
user.name = 'admin'
user.real_name = 'Administrador'
user.hash_password(password)

# load config
app.config.from_object(Config)

# load database
db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.add(user)
    db.session.commit()
