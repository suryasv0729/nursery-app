from flask import Blueprint, request, jsonify
from controllers.chat_controller import process_chat_message

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'message': "I didn't understand that."}), 400
    
    user_message = data['message']
    bot_reply = process_chat_message(user_message)
    
    return jsonify({'reply': bot_reply}), 200
