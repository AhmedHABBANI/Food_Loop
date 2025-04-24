from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, DateTimeField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from app.models.user import User
from datetime import datetime


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    business_name = StringField('Nom de l\'établissement', validators=[DataRequired()])
    business_type = SelectField('Type d\'établissement', 
                              choices=[('restaurant', 'Restaurant'), 
                                     ('supermarket', 'Supermarché')],
                              validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Répéter le mot de passe', 
                            validators=[DataRequired(), 
                                      EqualTo('password', message='Les mots de passe doivent correspondre')])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse email est déjà utilisée.')
        
class OfferForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=500)])
    initial_quantity = FloatField('Quantité initiale', validators=[DataRequired(), NumberRange(min=0.1)])
    unit = SelectField('Unité', choices=[
        ('kg', 'Kilogrammes'),
        ('units', 'Unités'),
        ('litres', 'Litres'),
        ('plates', 'Portions')
    ], validators=[DataRequired()])
    price = FloatField('Prix de vente', validators=[DataRequired(), NumberRange(min=0)])
    original_price = FloatField('Prix original', validators=[DataRequired(), NumberRange(min=0)])
    # Modification ici : utilisation de DateTimeLocalField au lieu de DateTimeField
    expiry_date = DateTimeLocalField(
        'Date de péremption',
        format='%Y-%m-%dT%H:%M',  # Format HTML5 datetime-local
        validators=[DataRequired()]
    )
    submit = SubmitField('Publier l\'offre')

    def validate_expiry_date(self, field):
        if field.data < datetime.now():
            raise ValidationError('La date de péremption doit être dans le futur')