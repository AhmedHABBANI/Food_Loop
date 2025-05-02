from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import datetime

class OfferForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(min=4, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    initial_quantity = FloatField('Quantité initiale', validators=[
        DataRequired(), 
        NumberRange(min=0.1, message="La quantité doit être supérieure à 0")
    ])
    unit = SelectField('Unité', choices=[
        ('kg', 'Kilogrammes'),
        ('units', 'Unités'),
        ('litres', 'Litres')
    ], validators=[DataRequired()])
    current_price = FloatField('Prix actuel (MAD)', validators=[
        DataRequired(), 
        NumberRange(min=0, message="Le prix doit être positif")
    ])
    original_price = FloatField('Prix original (MAD)', validators=[
        DataRequired(), 
        NumberRange(min=0, message="Le prix doit être positif")
    ])
    expiration_date = DateTimeField('Date d\'expiration', 
                                  format='%Y-%m-%dT%H:%M',  # Format pour l'input type datetime-local
                                  validators=[DataRequired()])
    submit = SubmitField('Créer l\'offre')