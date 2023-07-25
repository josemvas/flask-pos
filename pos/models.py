from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    real_name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    hourly_price = db.Column(db.Float, nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False)
    created_by = relationship("User", backref="transactions")
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    service = relationship("Service", backref="transactions")
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    service_duration = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(16), nullable=False)
    def __init__(self):
        self.created_on = datetime.now()
        self.created_by_id = current_user.get_id()
        self.status = "Paid"
