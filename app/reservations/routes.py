from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.reservations import bp
from app.models import Reservation, Offer
from datetime import datetime

@bp.route('/list')
@login_required
def list():
    # Récupérer les réservations où l'utilisateur est l'acheteur
    my_reservations = Reservation.query.filter_by(
        customer_id=current_user.id
    ).order_by(Reservation.created_at.desc()).all()
    
    # Récupérer les réservations où l'utilisateur est le vendeur
    received_reservations = Reservation.query.join(Offer).filter(
        Offer.seller_id == current_user.id
    ).order_by(Reservation.created_at.desc()).all()
    
    return render_template('reservations/list.html',
                         my_reservations=my_reservations,
                         received_reservations=received_reservations)

@bp.route('/create/<int:offer_id>', methods=['GET', 'POST'])
@login_required
def create(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    if request.method == 'POST':
        try:
            quantity = float(request.form.get('quantity', 0))
            pickup_date = datetime.strptime(request.form.get('pickup_date'), '%Y-%m-%dT%H:%M')
            
            if quantity <= 0 or quantity > offer.remaining_quantity:
                flash('Quantité invalide', 'error')
                return redirect(url_for('offers.detail', id=offer_id))
            
            reservation = Reservation(
                offer_id=offer_id,
                customer_id=current_user.id,
                quantity=quantity,
                pickup_date=pickup_date,
                status='pending'
            )
            
            # Mettre à jour la quantité restante
            offer.remaining_quantity -= quantity
            if offer.remaining_quantity <= 0:
                offer.status = 'reserved'
            
            db.session.add(reservation)
            db.session.commit()
            
            flash('Réservation effectuée avec succès!', 'success')
            return redirect(url_for('reservations.list'))
            
        except ValueError:
            flash('Données invalides', 'error')
            return redirect(url_for('offers.detail', id=offer_id))
    
    return redirect(url_for('offers.detail', id=offer_id))

@bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    reservation = Reservation.query.get_or_404(id)
    if reservation.customer_id != current_user.id:
        flash('Non autorisé', 'error')
        return redirect(url_for('reservations.list'))
    
    offer = Offer.query.get(reservation.offer_id)
    offer.remaining_quantity += reservation.quantity
    if offer.status == 'reserved':
        offer.status = 'available'
    
    reservation.status = 'cancelled'
    db.session.commit()
    
    flash('Réservation annulée', 'success')
    return redirect(url_for('reservations.list'))