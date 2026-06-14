from flask import Flask, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret')
    
    # Register blueprints 
    from routes.auth_routes import auth_bp
    from routes.product_routes import product_bp
    from routes.admin_routes import admin_bp
    from routes.cart_routes import cart_bp
    from routes.order_routes import order_bp
    from routes.contact_routes import contact_bp
    from routes.chat_routes import chat_bp
    from routes.tribute_routes import tribute_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(tribute_bp, url_prefix='/api/tribute')
    
    # Root endpoint - API information
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Nursery App API',
            'version': '1.0.0',
            'status': 'online',
            'endpoints': {
                'auth': '/api/auth',
                'products': '/api/products',
                'cart': '/api/cart',
                'orders': '/api/orders',
                'admin': '/api/admin',
                'contact': '/api/contact',
                'chat': '/api/chat',
                'tribute': '/api/tribute'
            },
            'documentation': 'See ROUTES_CREATED.md for full API documentation'
        }), 200
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
