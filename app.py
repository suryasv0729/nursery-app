from flask import Flask, render_template, request, jsonify
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
    
    # Serve Frontend Templates
    @app.route('/')
    def index():
        return render_template('index.html')
        
    @app.route('/products')
    def products():
        return render_template('products.html')
        
    @app.route('/product/<int:id>')
    def product_detail(id):
        return render_template('product_detail.html', product_id=id)
        
    @app.route('/cart')
    def cart():
        return render_template('cart.html')
        
    @app.route('/wishlist')
    def wishlist():
        return render_template('wishlist.html')
        
    @app.route('/checkout')
    def checkout():
        return render_template('checkout.html')
        
    @app.route('/admin/login')
    def admin_login():
        return render_template('admin/login.html')

    @app.route('/admin')
    def admin_dashboard():
        return render_template('admin/dashboard.html')
        
    @app.route('/orders')
    def order_history():
        return render_template('orders.html')
        
    @app.route('/contact')
    def contact_page():
        return render_template('contact.html')
        
    @app.route('/about')
    def about_page():
        return render_template('about.html')

    @app.route('/tribute')
    def tribute_page():
        return render_template('tribute.html')

    @app.route('/planting-tips')
    def planting_tips_page():
        return render_template('planting_tips.html')

    @app.route('/testimonials')
    def testimonials_page():
        return render_template('testimonials.html')

    @app.route('/reset-password')
    def reset_password_page():
        token = request.args.get('token')
        if not token:
            return "Invalid or missing token", 400
        return render_template('reset_password.html', token=token)
    
    # Health check endpoint for monitoring
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
