from flask_wtf import FlaskForm
from wtforms import FloatField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ReservationForm(FlaskForm):
    quantity = FloatField('Quantité', validators=[
        DataRequired(), 
        NumberRange(min=0.1, message="La quantité doit être supérieure à 0")
    ])
    pickup_date = DateTimeField('Date de récupération', format='%Y-%m-%d %H:%M', 
                              validators=[DataRequired()])
    submit = SubmitField('Confirmer la réservation')