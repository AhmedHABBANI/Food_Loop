from app import db
from datetime import datetime

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    initial_quantity = db.Column(db.Float, nullable=False)
    remaining_quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='available')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def update_status(self):
        if datetime.utcnow() > self.expiry_date:
            self.status = 'expired'
        elif self.remaining_quantity <= 0:
            self.status = 'sold_out'
        elif self.reservations.filter_by(status='confirmed').count() > 0:
            self.status = 'partially_reserved' if self.remaining_quantity > 0 else 'reserved'
        else:
            self.status = 'available'
        
    def get_status_badge_color(self):
        status_colors = {
            'available': 'success',
            'partially_reserved': 'warning',
            'reserved': 'primary',
            'sold_out': 'danger',
            'expired': 'secondary'
        }
        return status_colors.get(self.status, 'secondary')

    def __repr__(self):
        return f'<Offer {self.title}>'