from flask import Flask, render_template, redirect, url_for, request, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Laptop, Course 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laptop_rec.db'
app.config['SECRET_KEY'] = 'knec_project_2026'

db.init_app(app)

# --- NEW: Login Manager Setup (Mandatory) ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# --------------------------------------------

admin = Admin(app, name='Laptop System Admin')
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Laptop, db.session))

@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # FIX: Use Capital 'User'
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            # Redirect based on role
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('index')) # Or seller dashboard
    return render_template('login.html')

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash("Access Denied!")
        return redirect(url_for('index'))
    all_courses = Course.query.all()
    return render_template('student_dashboard.html', courses=all_courses, laptops=[])

@app.route('/search', methods=['POST'])
@login_required
def search():
    budget = request.form.get('max_budget')
    course_id = request.form.get('course_id')
    selected_course = Course.query.get(course_id)
    
    # Expert Logic: Filter by budget AND course requirements
    results = Laptop.query.filter(
        Laptop.price <= budget,
        Laptop.ram >= selected_course.min_ram
    ).all()
    
    return render_template('student_dashboard.html', 
                           laptops=results, 
                           courses=Course.query.all())

# FIX: This must be at the VERY BOTTOM
if __name__ == '__main__':
    app.run(debug=True)