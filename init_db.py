from app import app, db
from models import User, Laptop

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create admin user
        admin = User(username='Aristo', password='aristo123', role='admin')
        db.session.add(admin)
        db.session.flush()  # Get ID before commit

        # Create test users
        student = User(username='student1', password='pass123', role='student')
        seller = User(username='seller1', password='pass123', role='seller')
        db.session.add_all([student, seller])

        db.session.commit()
        print("Database initialized with admin: Aristo/aristo123")

if __name__ == "__main__":
    init_db()

