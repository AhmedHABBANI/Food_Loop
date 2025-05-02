from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    company_name = db.Column(db.String(120))
    company_type = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    offers = db.relationship('Offer', backref='seller', lazy='dynamic')
    reservations_made = db.relationship('Reservation', 
                                      foreign_keys='Reservation.customer_id',
                                      backref='customer', 
                                      lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Offer(db.Model):
    __tablename__ = 'offers'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    initial_quantity = db.Column(db.Float, nullable=False)
    remaining_quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reservations = db.relationship('Reservation', backref='offer', lazy='dynamic')

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    pickup_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'), nullable=False)