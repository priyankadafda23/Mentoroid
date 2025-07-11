from flask import Blueprint, request, jsonify
from models import db, Notification, User
from datetime import datetime

notif_bp = Blueprint('notifications', __name__)

@notif_bp.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    notifs = Notification.query.filter_by(recipient_id=user_id).order_by(Notification.timestamp.desc()).limit(20).all()
    return jsonify([
        {
            'id': n.id,
            'message': n.message,
            'is_read': n.is_read,
            'timestamp': n.timestamp.strftime('%Y-%m-%d %H:%M'),
        } for n in notifs
    ])

@notif_bp.route('/notifications/mark-read/<int:user_id>', methods=['POST'])
def mark_read(user_id):
    Notification.query.filter_by(recipient_id=user_id).update({'is_read': True})
    db.session.commit()
    return jsonify({'message': 'All marked as read'})
