from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models.offer import Offer
from app.forms import OfferForm
from datetime import datetime

offers_bp = Blueprint('offers', __name__)

@offers_bp.route('/offers')
def index():
    page = request.args.get('page', 1, type=int)
    offers = Offer.query.filter_by(status='available')\
        .order_by(Offer.created_at.desc())\
        .paginate(page=page, per_page=10)
    return render_template('offers/index.html', offers=offers)

@offers_bp.route('/offers/create', methods=['GET', 'POST'])
@login_required
def create():
    form = OfferForm()
    if form.validate_on_submit():
        offer = Offer(
            title=form.title.data,
            description=form.description.data,
            initial_quantity=form.initial_quantity.data,
            remaining_quantity=form.initial_quantity.data,
            unit=form.unit.data,
            price=form.price.data,
            original_price=form.original_price.data,
            expiry_date=form.expiry_date.data,
            author=current_user
        )
        db.session.add(offer)
        db.session.commit()
        flash('Votre offre a été publiée avec succès!')
        return redirect(url_for('offers.index'))
    return render_template('offers/create.html', form=form)

@offers_bp.route('/offers/<int:id>')
def show(id):
    offer = Offer.query.get_or_404(id)
    return render_template('offers/show.html', offer=offer)

@offers_bp.route('/my-offers')
@login_required
def my_offers():
    offers = Offer.query.filter_by(author=current_user)\
        .order_by(Offer.created_at.desc()).all()
    return render_template('offers/my_offers.html', offers=offers)