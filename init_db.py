from app import create_app, db
from app.models import User, Offer, Reservation

def init_database():
    app = create_app()
    with app.app_context():
        # Supprimer toutes les tables existantes
        db.drop_all()
        
        # Créer toutes les tables
        db.create_all()
        
        print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()