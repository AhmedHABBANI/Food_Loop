from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.offers import bp as offers_bp
    app.register_blueprint(offers_bp, url_prefix='/offers')

    from app.reservations import bp as reservations_bp
    app.register_blueprint(reservations_bp, url_prefix='/reservations')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app