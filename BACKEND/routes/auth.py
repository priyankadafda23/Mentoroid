from flask import Blueprint, request, jsonify
from models import db, User
import re
import hashlib
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask import current_app
import cloudinary


auth_bp = Blueprint('auth', __name__)
load_dotenv()

cloud = cloudinary.config(
    cloud_name=os.getenv("cloud_name"),
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("api_secret")
)

def is_valid_email(email):
    return re.match(r".+@(gmail|yahoo|outlook)\.com$", email)

def is_strong_password(pw):
    return re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', pw)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # 1. Get data
        data = request.form
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        name = data.get('name')
        image_file = request.files.get('image')  # Optional file

        print("Form Data:", email, password, role, name)

        # 2. Basic validations
        if not email or not password or not role:
            return jsonify({'error': 'Missing required fields'}), 400
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email'}), 400
        if not is_strong_password(password):
            return jsonify({'error': 'Weak password'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        # 3. Hash password
        hashed = hashlib.sha256(password.encode()).hexdigest()

        # 4. Upload image to Cloudinary
        image_url = None
        if image_file:
            result = cloud.uploader.upload(image_file)
            image_url = result.get("secure_url")

        # 5. Create user
        user = User(
            email=email,
            password=hashed,
            role=role,
            name=name,
            image=image_url
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Signup successful'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = hashlib.sha256(data['password'].encode()).hexdigest()

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user': {
        'name' : user.name,
        'id': user.id,
        'role': user.role,
        'email': user.email,
        'image': user.image
    }})
    
