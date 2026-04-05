from app import app, db
from models import User, Course, Laptop

with app.app_context():
    db.drop_all()   # Clears the old database
    db.create_all() # Rebuilds fresh tables
    # Define Aristo (Admin)
    aristo = User(username="Aristo", password="admin123", role="admin")
    # Define Alice
    alice = User(username="Alice", password="123", role="seller")
    # Define Daniel
    daniel = User(username="Daniel", password="123", role="student")

    
    # Add all to the session
    db.session.add(alice)
    db.session.add(daniel)
    db.session.add(aristo)
    
    # Push to the Database
    db.session.commit()
    
    # Confirm users exist by querying them back
    count = User.query.count()
    print(f"Success! Created {count} users.")
    print(f"Users in DB: {[user.username for user in User.query.all()]}")