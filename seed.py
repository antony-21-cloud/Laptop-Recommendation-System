from app import app, db
from models import User, Course, Laptop

with app.app_context():
    # This line is the magic. It creates the 'users', 'courses', and 'laptops' tables.
    db.create_all() 
    
    # Now add a test student so you can actually log in!
    test_student = User(
        username="Daniel", 
        password="123", 
        role="student"
    )
    
    db.session.add(test_student)
    db.session.commit()
    print("Database built and 'Daniel' created!")