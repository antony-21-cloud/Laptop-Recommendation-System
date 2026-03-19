from app import app, db
from models import Laptop, Course, Supplier

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database 'laptop_rec.db' created successfully!")