from flask import Blueprint, request, jsonify
from controllers.contact_controller import submit_contact, get_all_messages
from controllers.auth_controller import authorize

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/submit', methods=['POST'])
def submit():
    data = request.json
    res = submit_contact(data)
    if res:
        return jsonify({'message': 'Message sent successfully'}), 201
    return jsonify({'message': 'Failed to send message'}), 400

@contact_bp.route('/messages', methods=['GET'])
@authorize(role_required='admin')
def get_messages(current_user_id, current_user_role):
    messages = get_all_messages()
    return jsonify(messages), 200
