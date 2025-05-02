from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.offers import bp
from app.models import Offer
from app.offers.forms import OfferForm

@bp.route('/list')
def list():
    offers = Offer.query.filter(
        Offer.status == 'available',
        Offer.expiration_date > datetime.utcnow()
    ).order_by(Offer.created_at.desc()).all()
    return render_template('offers/list.html', offers=offers)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = OfferForm()
    if form.validate_on_submit():
        if form.current_price.data >= form.original_price.data:
            flash('Le prix actuel doit être inférieur au prix original', 'error')
            return render_template('offers/create.html', form=form)

        offer = Offer(
            title=form.title.data,
            description=form.description.data,
            initial_quantity=form.initial_quantity.data,
            remaining_quantity=form.initial_quantity.data,
            unit=form.unit.data,
            current_price=form.current_price.data,
            original_price=form.original_price.data,
            expiration_date=form.expiration_date.data,
            seller=current_user,
            status='available'
        )
        db.session.add(offer)
        db.session.commit()
        flash('Votre offre a été créée avec succès!', 'success')
        return redirect(url_for('offers.list'))
    
    return render_template('offers/create.html', form=form)

@bp.route('/<int:id>')
def detail(id):
    offer = Offer.query.get_or_404(id)
    return render_template('offers/detail.html', offer=offer)