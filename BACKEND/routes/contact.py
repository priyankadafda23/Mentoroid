from flask import Blueprint, request, jsonify
from models import db
from datetime import datetime

contact_bp = Blueprint('contact', __name__)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    subject = db.Column(db.String(150))
    message = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        new_message = ContactMessage(
            name=data['name'],
            email=data['email'],
            mobile=data['mobile'],
            subject=data['subject'],
            message=data['message']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Form submitted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
