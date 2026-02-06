from flask import Flask, request, jsonify
from config import Config
from models import db, User, Attendance
from utils import get_face_encoding_from_file, identify_user
from datetime import datetime
import traceback

app = Flask(__name__)
app.config.from_object(Config)

# CORS: allow frontend to call this API
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Initialize DB
db.init_app(app)

# Create tables before running (Run once)
try:
    with app.app_context():
        db.create_all()
        print("✓ Database tables created/verified successfully")
except Exception as e:
    print(f"⚠ Warning: Could not create database tables: {e}")
    print("  Make sure MySQL is running and the database exists.")

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        return '', 200

@app.route('/')
def home():
    return "Face Attendance Backend is Running!"

# --- 1. REGISTER USER ---
@app.route('/register', methods=['POST'])
def register():
    """
    Expects form-data:
    - name: text
    - email: text
    - image: file
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    name = request.form.get('name')
    email = request.form.get('email')
    file = request.files['image']

    # 1. Process Image
    encoding = get_face_encoding_from_file(file)
    if encoding is None:
        return jsonify({"error": "No face detected in the image. Please try again."}), 400

    # 2. Validate inputs
    if not name or not name.strip():
        return jsonify({"error": "Name is required"}), 400
    if not email or not email.strip():
        return jsonify({"error": "Email is required"}), 400
    
    # 3. Save to DB
    try:
        # Check if email already exists
        existing_user = User.query.filter_by(email=email.strip()).first()
        if existing_user:
            return jsonify({"error": f"Email {email} is already registered"}), 400
        
        new_user = User(name=name.strip(), email=email.strip(), face_encoding=encoding)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": f"User {name.strip()} registered successfully!",
            "id": new_user.id
        }), 201
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        if "Duplicate entry" in error_msg or "UNIQUE constraint" in error_msg:
            return jsonify({"error": "Email already exists in database"}), 400
        print(f"Registration error: {traceback.format_exc()}")
        return jsonify({"error": f"Database error: {error_msg}"}), 500

# --- 2. MARK ATTENDANCE ---
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    """
    Expects form-data:
    - image: file (Live capture)
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']

    # 1. Get Live Encoding
    live_encoding = get_face_encoding_from_file(file)
    if live_encoding is None:
        return jsonify({"error": "No face detected"}), 400

    # 2. Fetch all users from DB to compare
    users = User.query.all()
    known_users_data = [(u.id, u.face_encoding) for u in users]

    # 3. Identify User
    user_id = identify_user(live_encoding, known_users_data)

    if user_id:
        # 4. Check if already attended TODAY
        today = datetime.utcnow().date()
        existing_record = Attendance.query.filter_by(user_id=user_id, date=today).first()

        if existing_record:
            return jsonify({
                "status": "success",
                "message": "Attendance already marked for today.",
                "user_id": user_id
            }), 200
        
        # 5. Mark Attendance
        try:
            new_attendance = Attendance(user_id=user_id)
            db.session.add(new_attendance)
            db.session.commit()
            
            # Fetch user name for response
            user = User.query.get(user_id)
            return jsonify({
                "status": "success",
                "message": f"Welcome {user.name}, attendance marked!",
                "user_id": user_id,
                "user_name": user.name
            }), 200
        except Exception as e:
            db.session.rollback()
            print(f"Attendance marking error: {traceback.format_exc()}")
            return jsonify({"error": f"Failed to save attendance: {str(e)}"}), 500
    else:
        return jsonify({"status": "failed", "message": "User not recognized. Please register first."}), 404

# --- 3. GET LOGS ---
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        logs = Attendance.query.order_by(Attendance.timestamp.desc()).limit(100).all()
        output = []
        for log in logs:
            output.append({
                "user": log.user.name,
                "email": log.user.email,
                "time": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "date": log.date.strftime("%Y-%m-%d")
            })
        return jsonify(output)
    except Exception as e:
        print(f"Logs error: {traceback.format_exc()}")
        return jsonify({"error": f"Failed to fetch logs: {str(e)}"}), 500

# --- 4. GET USERS LIST ---
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        output = []
        for user in users:
            output.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return jsonify(output)
    except Exception as e:
        print(f"Users list error: {traceback.format_exc()}")
        return jsonify({"error": f"Failed to fetch users: {str(e)}"}), 500

# --- 5. HEALTH CHECK ---
@app.route('/health', methods=['GET'])
def health():
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "message": "Backend is running properly"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 503

if __name__ == '__main__':
    app.run(debug=True, port=5000)