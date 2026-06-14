from flask import Blueprint, request, jsonify
from utils.db import get_db_connection

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject', 'No Subject')
        message = data.get('message')
        
        if not name or not email or not message:
            return jsonify({'error': 'Name, email, and message are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
            (name, email, subject, message)
        )
        conn.commit()
        message_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Message sent successfully',
            'message_id': message_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
