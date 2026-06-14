from flask import Blueprint, request, jsonify

chat_bp = Blueprint('chat', __name__)

# Simple chatbot responses
RESPONSES = {
    'greeting': [
        'Hello! Welcome to our Nursery. How can I help you today?',
        'Hi there! I can help you find the perfect plants for your garden.',
        'Welcome! Feel free to ask me about our plants, care tips, or placing orders.'
    ],
    'plants': [
        'We have a wide variety of plants including flowering plants, medicinal herbs, and ornamental plants. What are you looking for?',
        'Our collection includes indoor plants, outdoor plants, and seasonal flowers. Would you like to know more about any specific category?'
    ],
    'care': [
        'Plant care varies by species. Generally, most plants need adequate sunlight, water, and well-draining soil. Which plant would you like to know about?',
        'Basic plant care includes proper watering, fertilizing, and pest control. What specific care information do you need?'
    ],
    'order': [
        'You can browse our products and add them to your cart. Checkout is simple and secure!',
        'To place an order, select your desired plants, add them to cart, and proceed to checkout. We deliver fresh plants to your doorstep.'
    ],
    'default': [
        'I\'m here to help! You can ask me about our plants, plant care, or how to place an order.',
        'I can assist you with product information, care tips, and ordering process. What would you like to know?',
        'Feel free to ask me anything about our nursery, plants, or services!'
    ]
}

def get_response(message):
    message = message.lower()
    
    if any(word in message for word in ['hi', 'hello', 'hey', 'greetings']):
        return RESPONSES['greeting'][0]
    elif any(word in message for word in ['plant', 'flower', 'tree', 'herb', 'product']):
        return RESPONSES['plants'][0]
    elif any(word in message for word in ['care', 'water', 'soil', 'sunlight', 'fertilizer', 'grow']):
        return RESPONSES['care'][0]
    elif any(word in message for word in ['order', 'buy', 'purchase', 'cart', 'checkout']):
        return RESPONSES['order'][0]
    else:
        return RESPONSES['default'][0]

@chat_bp.route('/message', methods=['POST'])
def chat_message():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        bot_response = get_response(user_message)
        
        return jsonify({
            'message': user_message,
            'response': bot_response
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
