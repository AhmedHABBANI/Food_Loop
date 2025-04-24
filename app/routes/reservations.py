from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models.reservation import Reservation
from app.models.offer import Offer

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('/my-reservations')
@login_required
def my_reservations():
    return render_template('reservations/my_reservations.html')