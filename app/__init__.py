from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import des blueprints
    from app.routes.auth import auth_bp
    from app.routes.offers import offers_bp
    from app.routes.reservations import reservations_bp

    # Enregistrement des blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(offers_bp)
    app.register_blueprint(reservations_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app