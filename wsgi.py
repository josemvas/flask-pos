from pos import app
from pos.models import db
from pos.views import root, users, services, transactions
from pos.auth import login_manager
from config import Config

# load config
app.config.from_object(Config)

# load database
db.init_app(app)

# use login
login_manager.init_app(app)

# register blueprints
app.register_blueprint(root.bp)
app.register_blueprint(users.bp)
app.register_blueprint(services.bp)
app.register_blueprint(transactions.bp)

if __name__ == '__main__':
    app.run()
