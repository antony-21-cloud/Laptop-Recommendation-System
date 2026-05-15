import os
import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

# 1. Import ONLY the db and models from your models file
from models import db, User, Laptop, SupportTicket, PurchaseRequest
from datetime import datetime, timezone

app = Flask(__name__)

import os
from werkzeug.utils import secure_filename
import time


# 2. Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'knec_project_2026'  # Flask session encryption key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'laptop_rec.db')  # SQLite database path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system for performance
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')  # Where uploaded laptop images are stored
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit for uploads - prevents large file attacks
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Valid image formats for laptop photos

# Create upload folder if it doesn't exist (prevents file save errors)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Validate if uploaded file has an allowed image extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 3. LINK the existing db to this app (This is the only line you need)
db.init_app(app) 

## 4. INITIALIZE LoginManager - Handles user session management
login_manager = LoginManager()
login_manager.login_view = 'login'  # type: ignore Redirect to login page if user tries to access protected route
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Load user from database by ID for Flask-Login session management"""
    return db.session.get(User, int(user_id))

# 5. CREATE tables - Creates all database tables if they don't exist
with app.app_context():
    db.create_all()

# --- 1. ADMIN SECURITY ---
class MyAdminView(ModelView):
    """Custom admin view that restricts access to only the main admin user 'Aristo'"""
    def is_accessible(self):
        # Checks if user is logged in AND is either the 'Aristo' user or has admin role
        return current_user.is_authenticated and (current_user.username == 'Aristo')

    def inaccessible_callback(self, name, **kwargs):
        # Kick them out if they aren't authorized
        return redirect(url_for('login'))
    

class MyAdminHomeView(AdminIndexView):
    """Custom admin home page with statistics dashboard"""
    @expose('/')
    def index(self):
        user_count = User.query.count()  # Total registered users
        laptop_count = Laptop.query.count()  # Total laptops in system
        all_users = User.query.all()  # List of all users for display
        return self.render('admin/index.html', 
            user_count=user_count, 
            laptop_count=laptop_count,
            users=all_users)


# Set the configuration directly on the app to avoid the init error
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'  # UI theme for admin panel

# Initialize Admin without the problematic keyword
admin = Admin(app, name='Laptop System Admin', index_view=MyAdminHomeView(url='/admin'))

# Add your views on separate lines - allows CRUD operations on these models
admin.add_view(MyAdminView(User, db.session))
admin.add_view(MyAdminView(Laptop, db.session))
admin.add_view(MyAdminView(SupportTicket, db.session))


@app.route('/')
def index():
    """Public landing page - first page users see"""
    return render_template('index.html')



# --- 3. NAVIGATION & LOGIC ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login - authenticates credentials and redirects based on role"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()  # Find user by username
        
        if user and user.password == password:  # Simple password check (consider hashing for production)
            login_user(user)  # Start user session
            print(f"✅ User logged in: {user.username}, Role: {user.role}")  # Debug
            
            # Redirect to appropriate dashboard based on user role
            if user.role == 'admin' or user.username == 'Aristo':
                return redirect(url_for('admin_dashboard'))  # Admin goes to admin panel
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))  # Student goes to browse laptops
            elif user.role == 'seller':
                return redirect(url_for('seller_dashboard'))  # Seller goes to manage listings
            else:
                # Fallback for any other role
                return redirect(url_for('student_dashboard'))
        
        flash('Invalid credentials. Try again.')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration - creates student or seller account"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('role', 'student')
        
        # Ensure role is either 'student' or 'seller' (prevent invalid roles)
        if selected_role not in ['student', 'seller']:
            selected_role = 'student'
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('register'))
        
        # Create user with the selected role
        new_user = User(username=username, password=password, role=selected_role)
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"Registration successful! You are registered as a {selected_role}.")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/seller_dashboard')
@login_required
def seller_dashboard():
    """Seller's main dashboard - shows their listed laptops and inquiries"""
    # Only allow users with role 'seller' or admin user 'Aristo'
    if current_user.role != 'seller' and current_user.username != 'Aristo':
        flash("Access denied. Seller dashboard is for sellers only.")
        return redirect(url_for('student_dashboard'))
    
    # Get only laptops belonging to this seller (filter by seller_id)
    my_laptops = Laptop.query.filter_by(seller_id=current_user.id).all()
    return render_template('seller_dashboard.html', laptops=my_laptops, count=len(my_laptops))

@app.route('/student_dashboard', methods=['GET', 'POST'])
@login_required
def student_dashboard():
    """Student's main dashboard - browse and search laptops"""
    laptops = Laptop.query.all()  # Get all laptops for display
    # Convert laptops to serializable format with images (for JSON API compatibility)
    laptop_list = []
    for laptop in laptops:
        seller = User.query.get(laptop.seller_id)  # Get seller info for each laptop
        laptop_list.append({
            'id': laptop.id,
            'name': laptop.name,
            'processor_type': laptop.processor_type,
            'ram': laptop.ram,
            'specs': laptop.specs,
            'price': laptop.price,
            'seller_id': laptop.seller_id,
            'seller_name': seller.username if seller else 'Unknown',
            'image': getattr(laptop, 'image', None)  # Include image path if exists
        })
    return render_template('student_dashboard.html', laptops=laptop_list)

def get_requirements_by_course(course_name):
    """
    Course-based laptop recommendation logic.
    Maps academic courses to recommended processor types.
    """
    if not course_name:
        return {'pref_cpu': 'Any'}
    
    course = course_name.lower()
    
    # 1. SMART LOGIC: Define hardware rules based on the user's course
    if any(word in course for word in ['cyber', 'ict', 'computer']):
        return {'pref_cpu': 'Ryzen 7'}  # High-performance for technical courses
    
    elif any(word in course for word in ['law', 'journ', 'bus']):
        return {'pref_cpu': 'Core i5'}  # Mid-range for business/law
    
    elif any(word in course for word in ['design', 'art', 'video']):
        return {'pref_cpu': 'M2'}  # Apple Silicon for creative work
        
    return {'pref_cpu': 'Any'}  # Default recommendation

@app.route('/api/update-profile', methods=['POST'])
@login_required
def update_profile():
    """API endpoint for students to update their profile information"""
    data = request.get_json()
    
    # Update only the fields that exist in your User model (partial update)
    if 'name' in data:
        current_user.name = data['name']
    if 'email' in data:
        current_user.email = data['email']
    if 'field_of_study' in data:
        current_user.field_of_study = data['field_of_study']
    if 'institution' in data:
        current_user.institution = data['institution']
    if 'preferred_brands' in data:
        current_user.preferred_brands = data['preferred_brands']
    if 'preferred_specs' in data:
        current_user.preferred_specs = data['preferred_specs']
    if 'purpose' in data:
        current_user.purpose = data['purpose']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/search', methods=['GET'])
@login_required
def api_search_laptops():
    """
    Search API for students to filter laptops.
    Supports filters: processor, field_of_study (course), budget, min RAM
    """
    processor = request.args.get('processor', '').strip()
    field_of_study = request.args.get('field_of_study', '').strip()
    budget = request.args.get('budget', '').strip()
    ram_filter = request.args.get('ram', '').strip()

    query = Laptop.query  # Start with all laptops

    # Apply filters only if values are provided
    if processor and processor != 'All':
        query = query.filter(Laptop.processor_type.ilike(f'%{processor}%'))  # Case-insensitive partial match
    if field_of_study:
        query = query.filter(Laptop.specs.ilike(f'%{field_of_study}%'))  # Search within specs
    if budget:
        try:
            max_price = float(budget)
            query = query.filter(Laptop.price <= max_price)  # Budget cap
        except:
            pass
    if ram_filter:
        try:
            min_ram = int(ram_filter)
            if min_ram > 0:
                query = query.filter(Laptop.ram >= min_ram)  # Minimum RAM requirement
        except:
            pass

    laptops = query.all()
    
    # Build response with all fields needed by frontend
    result = []
    for laptop in laptops:
        seller = db.session.get(User, laptop.seller_id)
        result.append({
            'id': laptop.id,
            'name': laptop.name,
            'brand': getattr(laptop, 'brand', laptop.name.split()[0] if ' ' in laptop.name else laptop.name),
            'model': laptop.name,
            'processor': laptop.processor_type,
            'ram': laptop.ram,
            'storage': getattr(laptop, 'storage', '?'),
            'gpu': getattr(laptop, 'gpu', 'Integrated'),
            'price': laptop.price,
            'specs': laptop.specs,
            'seller_id': laptop.seller_id,
            'seller_name': seller.username if seller else 'Unknown',
            'image': getattr(laptop, 'image', None)  # Include image URL
        })
    
    return jsonify(result)


@app.route('/inquire', methods=['POST'])
@login_required
def inquire_laptop():
    """
    Student sends inquiry message to seller about a specific laptop.
    Creates a PurchaseRequest record in the database.
    """
    data = request.get_json()
    laptop_id = data.get('laptop_id')
    message = data.get('message', '').strip()

    if not laptop_id:
        return jsonify({"error": "Laptop ID required"}), 400

    laptop = Laptop.query.get(laptop_id)
    if not laptop:
        return jsonify({"error": "Laptop not found"}), 404

    # Prevent students from inquiring about their own laptops
    if laptop.seller_id == current_user.id:
        return jsonify({"error": "You cannot inquire about your own laptop"}), 400

    # Create purchase request (stores message for seller to see)
    new_request = PurchaseRequest(
        student_id=current_user.id,
        laptop_id=laptop.id,
        seller_id=laptop.seller_id,
        status='Pending',
        message=message
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Inquiry sent successfully!"}), 200


@app.route('/api/my-requests/<int:user_id>')
@login_required
def get_my_requests(user_id):
    """API endpoint for students to view their own inquiries/purchase requests"""
    try:
        # Security check - users can only see their own requests
        if user_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
        
        # Get all purchase requests for this student
        requests = PurchaseRequest.query.filter_by(student_id=user_id).all()
        
        # Convert to JSON
        result = []
        for r in requests:
            result.append({
                'id': r.id,
                'laptop_id': r.laptop_id,
                'seller_id': r.seller_id,
                'status': r.status,
                'message': getattr(r, 'message', ''),
                'created_at': r.created_at.isoformat() if hasattr(r, 'created_at') and r.created_at else None
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_my_requests: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/submit_support', methods=['POST'])
@login_required
def submit_support():
    """Users submit support tickets to admin"""
    sub = request.form.get('subject')
    msg = request.form.get('message')
    new_ticket = SupportTicket(user_id=current_user.id, subject=sub, message=msg)
    db.session.add(new_ticket)
    db.session.commit()
    flash("Support request sent to Admin!", "success")
    return redirect(url_for('student_dashboard'))


# Add these routes to your app.py
@app.route('/api/laptop', methods=['POST'])
@login_required
def api_add_laptop():
    """
    Seller uploads a new laptop listing.
    Handles both form data and image file upload.
    """
    try:
        print("="*50)
        print("UPLOAD RECEIVED")
        
        # Extract form data
        name = request.form.get('name')
        brand = request.form.get('brand')
        processor_type = request.form.get('processor_type')
        ram = request.form.get('ram')
        storage = request.form.get('storage')
        gpu = request.form.get('gpu')
        specs = request.form.get('specs')
        price = request.form.get('price')
        stock_status = request.form.get('stock_status', 'in-stock')
        
        print(f"Name: {name}")
        print(f"Price: {price}")
        
        # Create laptop object (saves to database)
        laptop = Laptop(
            name=name,
            processor_type=processor_type,
            specs=specs or '',
            price=price,
            seller_id=current_user.id
        )
        
        # Set optional fields if provided
        if ram:
            laptop.ram = int(ram)
        if storage:
            laptop.storage = storage
        if gpu:
            laptop.gpu = gpu
        if brand:
            laptop.brand = brand
        if stock_status:
            laptop.stock_status = stock_status
        
        # Handle image upload - saves to static/uploads/ folder
        if 'image' in request.files:
            file = request.files['image']
            print(f"Image file: {file.filename}")
            
            if file and file.filename:
                import time
                import os
                from werkzeug.utils import secure_filename
                
                # Create folder if not exists
                folder = os.path.join('static', 'uploads')
                os.makedirs(folder, exist_ok=True)
                
                # Save file with unique name (timestamp prevents collisions)
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{current_user.id}_{int(time.time())}.{ext}"
                filepath = os.path.join(folder, filename)
                file.save(filepath)
                laptop.image = f"/static/uploads/{filename}"  # Store URL path in database
                print(f"✅ Image saved: {laptop.image}")
        else:
            print("No image in request")
        
        db.session.add(laptop)
        db.session.commit()
        print(f"✅ Laptop ID: {laptop.id}")
        print("="*50)
        
        return jsonify({'message': 'Success', 'id': laptop.id}), 201
        
    except Exception as e:
        print(f"ERROR: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@app.route('/api/laptop/<int:laptop_id>', methods=['PUT'])
@login_required
def api_update_laptop(laptop_id):
    """Seller updates an existing laptop listing"""
    laptop = Laptop.query.get_or_404(laptop_id)
    # Security - only the seller who owns this laptop can edit it
    if laptop.seller_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    # Update only fields that are provided
    laptop.name = data.get('name', laptop.name)
    laptop.price = data.get('price', laptop.price)
    laptop.processor_type = data.get('processor_type', laptop.processor_type)
    laptop.ram = data.get('ram', laptop.ram)
    laptop.specs = data.get('specs', laptop.specs)
    db.session.commit()
    return jsonify({'message': 'Laptop updated successfully'})


@app.route('/api/laptop/<int:laptop_id>', methods=['DELETE'])
@app.route('/api/laptop/<int:laptop_id>', methods=['DELETE'])
@login_required
def api_delete_laptop(laptop_id):
    """Seller deletes a laptop listing (also removes associated image file)"""
    laptop = Laptop.query.get_or_404(laptop_id)
    # Security - only the seller who owns this laptop can delete it
    if laptop.seller_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Delete the image file if it exists (prevents orphaned files)
    if laptop.image and laptop.image.startswith('/static/uploads/'):
        import os
        filepath = os.path.join('.', laptop.image.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(laptop)
    db.session.commit()
    return jsonify({'message': 'Laptop deleted successfully'})

@app.route('/api/laptop/<int:laptop_id>', methods=['GET'])
@login_required
def api_get_laptop(laptop_id):
    """Get detailed information about a specific laptop"""
    laptop = Laptop.query.get_or_404(laptop_id)
    seller = db.session.get(User, laptop.seller_id)
    return jsonify({
        'id': laptop.id,
        'name': laptop.name,
        'price': laptop.price,
        'processor_type': laptop.processor_type,
        'ram': laptop.ram,
        'specs': laptop.specs,
        'seller_id': laptop.seller_id,
        'seller_name': seller.username if seller else 'Unknown',
        'image': getattr(laptop, 'image', None)
    })

@app.route('/api/user/<int:user_id>', methods=['GET'])
@login_required
def api_get_user(user_id):
    """Get basic user information by ID (used for inquiries display)"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role
    })



@app.route('/api/seller-requests/<int:seller_id>')
@login_required
def api_get_seller_requests(seller_id):
    """
    API endpoint for sellers to view inquiries about their laptops.
    Returns all purchase requests where this user is the seller.
    """
    # Security - sellers can only see their own inquiries (admin can see all)
    if current_user.id != seller_id and current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get requests where current user is the seller, ordered newest first
    requests = PurchaseRequest.query.filter_by(seller_id=seller_id).order_by(PurchaseRequest.id.desc()).all()
    
    result = []
    for r in requests:
        result.append({
            'id': r.id,
            'student_id': r.student_id,
            'laptop_id': r.laptop_id,
            'status': r.status,
            'message': getattr(r, 'message', None),
            'seller_reply': getattr(r, 'seller_reply', None),
            'replied_at': r.replied_at.isoformat() if hasattr(r, 'replied_at') and r.replied_at else None,
            'reply_status': getattr(r, 'reply_status', 'pending'),
            'created_at': r.created_at.isoformat() if hasattr(r, 'created_at') and r.created_at else None
        })
    
    return jsonify(result)

@app.route('/api/update-seller-profile', methods=['POST'])
@login_required
def update_seller_profile():
    """API endpoint for sellers to update their business profile information"""
    if current_user.role != 'seller':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update seller-specific fields
    if 'business_name' in data:
        current_user.business_name = data['business_name']
    if 'registration_number' in data:
        current_user.registration_number = data['registration_number']
    if 'email' in data:
        current_user.email = data['email']
    if 'phone' in data:
        current_user.phone = data['phone']
    if 'business_type' in data:
        current_user.business_type = data['business_type']
    if 'address' in data:
        current_user.address = data['address']
    if 'warranty_info' in data:
        current_user.warranty_info = data['warranty_info']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

# ==================== ADMIN API ROUTES ====================

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard - only accessible by 'Aristo' user"""
    if current_user.username != 'Aristo':
        flash('Access denied. Admin only.')
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html')

@app.route('/api/admin/stats')
@login_required
def admin_stats():
    """Admin API - get system statistics for dashboard"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    total_users = User.query.count()
    total_laptops = Laptop.query.count()
    unread_messages = SupportTicket.query.filter_by(status='Open').count()
    active_inquiries = PurchaseRequest.query.filter_by(status='Pending').count()
    
    return jsonify({
        'total_users': total_users,
        'total_laptops': total_laptops,
        'unread_messages': unread_messages,
        'active_inquiries': active_inquiries
    })

@app.route('/api/admin/users')
@login_required
def admin_users():
    """Admin API - get list of all users"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': getattr(u, 'email', None),
        'role': u.role,
        'is_active': True,
        'created_at': u.created_at.isoformat() if u.created_at else None
    } for u in users])

@app.route('/api/admin/laptops')
@login_required
def admin_laptops():
    """Admin API - get list of all laptops with seller information"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    laptops = Laptop.query.all()
    result = []
    for laptop in laptops:
        seller = db.session.get(User, laptop.seller_id)
        result.append({
            'id': laptop.id,
            'name': laptop.name,
            'processor_type': laptop.processor_type,
            'price': laptop.price,
            'stock_status': getattr(laptop, 'stock_status', 'in-stock'),
            'seller_id': laptop.seller_id,
            'seller_name': seller.username if seller else 'Unknown'
        })
    return jsonify(result)

@app.route('/api/admin/support-messages')
@login_required
def admin_support_messages():
    """Admin API - get all support tickets from users"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    messages = SupportTicket.query.order_by(SupportTicket.id.desc()).all()
    result = []
    for msg in messages:
        user = User.query.get(msg.user_id)
        result.append({
            'id': msg.id,
            'user_id': msg.user_id,
            'username': user.username if user else 'Unknown',
            'role': user.role if user else 'Unknown',
            'subject': msg.subject,
            'message': msg.message,
            'status': msg.status,
            'created_at': msg.created_at.isoformat() if hasattr(msg, 'created_at') else None
        })
    return jsonify(result)

@app.route('/api/admin/inquiries')
@login_required
def admin_inquiries():
    """Admin API - get all purchase requests/inquiries in the system"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    inquiries = PurchaseRequest.query.order_by(PurchaseRequest.id.desc()).all()
    result = []
    for inq in inquiries:
        student = User.query.get(inq.student_id)
        laptop = Laptop.query.get(inq.laptop_id)
        seller = User.query.get(inq.seller_id)
        result.append({
            'id': inq.id,
            'student_name': student.username if student else 'Unknown',
            'seller_name': seller.username if seller else 'Unknown',
            'laptop_name': laptop.name if laptop else 'Unknown',
            'message': getattr(inq, 'message', None),
            'status': inq.status,
            'created_at': inq.created_at.isoformat() if hasattr(inq, 'created_at') else None
        })
    return jsonify(result)

@app.route('/api/admin/reply-message', methods=['POST'])
@login_required
def admin_reply_message():
    """Admin API - reply to user support tickets"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    message_id = data.get('message_id')
    reply = data.get('reply')
    
    # Update message status to 'Replied'
    message = SupportTicket.query.get(message_id)
    if message:
        message.status = 'Replied'
        db.session.commit()
    
    # Here you would also send an email or store the reply
    # For now, just update status
    
    return jsonify({'message': 'Reply sent'}), 200

@app.route('/api/admin/mark-read/<int:message_id>', methods=['PATCH'])
@login_required
def admin_mark_read(message_id):
    """Admin API - mark support message as read"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    message = SupportTicket.query.get(message_id)
    if message:
        message.status = 'Read'
        db.session.commit()
    
    return jsonify({'message': 'Marked as read'}), 200

@app.route('/api/admin/delete-user/<int:user_id>', methods=['DELETE'])
@login_required
def admin_delete_user(user_id):
    """Admin API - delete a user account"""
    if current_user.username != 'Aristo':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if user and user.username != 'Aristo':  # Prevent deleting self
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    
    return jsonify({'error': 'Cannot delete this user'}), 400

@app.route('/api/reply-to-inquiry', methods=['POST'])
@login_required
def reply_to_inquiry():
    """Seller replies to a student's inquiry"""
    try:
        data = request.get_json()
        request_id = data.get('request_id')
        reply_message = data.get('reply_message', '').strip()
        
        if not request_id or not reply_message:
            return jsonify({'error': 'Missing request ID or reply message'}), 400
        
        # Get the purchase request
        inquiry = PurchaseRequest.query.get(request_id)
        if not inquiry:
            return jsonify({'error': 'Inquiry not found'}), 404
        
        # Verify the current user is the seller
        if inquiry.seller_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update the inquiry with seller's reply
        inquiry.seller_reply = reply_message
        from datetime import datetime
        inquiry.replied_at = datetime.now()
        inquiry.reply_status = 'replied'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Reply sent successfully',
            'reply': reply_message,
            'replied_at': inquiry.replied_at.isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error in reply_to_inquiry: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    """Log out user and end session"""
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)  # Run Flask in debug mode for development