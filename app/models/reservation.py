from app import db
from datetime import datetime

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pickup_time = db.Column(db.DateTime, nullable=False)
    
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    offer = db.relationship('Offer', backref='reservations')
    customer = db.relationship('User', backref='reservations')