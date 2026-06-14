import os
from utils.db import get_db_connection
from utils.mail import send_email

# Try to import razorpay, but don't fail if it's not available
try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False
    razorpay = None

KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')

# Treat placeholder values as empty
has_razorpay_keys = bool(RAZORPAY_AVAILABLE and KEY_ID and KEY_SECRET and KEY_ID != 'test_key_here')

if has_razorpay_keys:
    try:
        razorpay_client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    except Exception as e:
        print(f"Warning: Could not initialize Razorpay client: {e}")
        razorpay_client = None
        has_razorpay_keys = False
else:
    razorpay_client = None

def create_order(user_id, data):
    # data can have shipping_address and mobile_number
    shipping_address = data.get('shipping_address', '')
    mobile_number = data.get('mobile_number', '')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Calculate total amount from cart
            cursor.execute('''
                SELECT c.product_id, c.quantity, p.price, p.name 
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            ''', (user_id,))
            cart_items = cursor.fetchall()
            
            if not cart_items:
                return {'status': 400, 'data': {'message': 'Cart is empty'}}
                
            total_amount = sum(float(item['price']) * item['quantity'] for item in cart_items)
            
            amount_in_paise = int(total_amount * 100)
            
            if has_razorpay_keys:
                razorpay_order = razorpay_client.order.create({
                    "amount": amount_in_paise,
                    "currency": "INR",
                    "payment_capture": "1"
                })
                rzp_order_id = razorpay_order['id']
            else:
                import uuid
                rzp_order_id = f"mock_order_{uuid.uuid4().hex[:10]}"
            
            # Save order in DB
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount, razorpay_order_id, shipping_address, mobile_number) VALUES (%s, %s, %s, %s, %s)",
                (user_id, total_amount, rzp_order_id, shipping_address, mobile_number)
            )
            order_id = cursor.lastrowid
            
            # Save order items
            for item in cart_items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, item['product_id'], item['quantity'], item['price'])
                )
                
            conn.commit()
            
            return {'status': 200, 'data': {
                'order_id': order_id, 
                'razorpay_order_id': rzp_order_id,
                'amount': total_amount,
                'key_id': KEY_ID,
                'mock_mode': not has_razorpay_keys
            }}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': {'message': 'Order creation failed'}}
    finally:
        conn.close()

def verify_payment(data):
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')
    is_mock = data.get('mock_mode', False)
    
    if is_mock or not has_razorpay_keys:
        # Accept the payment blindly in mock mode
        pass
    else:
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            # Catch any razorpay errors or signature verification failures
            print(f"Payment verification error: {e}")
            return {'status': 400, 'data': {'message': 'Signature verification failed'}}
        
    # Signature is valid, update order status
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE orders SET status = 'paid', razorpay_payment_id = %s, razorpay_signature = %s WHERE razorpay_order_id = %s",
                (razorpay_payment_id, razorpay_signature, razorpay_order_id)
            )
            
            cursor.execute("SELECT id, user_id FROM orders WHERE razorpay_order_id = %s", (razorpay_order_id,))
            order = cursor.fetchone()
            
            if order:
                # Clear cart
                cursor.execute("DELETE FROM cart WHERE user_id = %s", (order['user_id'],))
                
                # Fetch user email
                cursor.execute("SELECT email, name FROM users WHERE id = %s", (order['user_id'],))
                user = cursor.fetchone()
                
                # Send confirmation email
                if user:
                    send_email(
                        to=user['email'], 
                        subject="Order Confirmation - Nursery App", 
                        body=f"Hello {user['name']},\n\nYour order (ID: {order['id']}) has been placed successfully and payment is verified.\n\nThank you for shopping with us!"
                    )
            
            conn.commit()
            return {'status': 200, 'data': {'message': 'Payment verified successfully'}}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': {'message': 'Database error during verification'}}
    finally:
        conn.close()

def get_user_orders(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
            orders = cursor.fetchall()
            
            for index, order in enumerate(orders):
                cursor.execute('''
                    SELECT oi.quantity, oi.price, p.name 
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                ''', (order['id'],))
                orders[index]['items'] = cursor.fetchall()
                
            return orders
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()


def cancel_order(order_id, user_id, reason="No reason provided"):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, user_id))
            order = cursor.fetchone()
            
            if not order:
                return {'status': 404, 'data': {'message': 'Order not found'}}
                
            if order['status'] in ['delivered', 'cancelled']:
                return {'status': 400, 'data': {'message': f"Order cannot be cancelled as it is already {order['status']}"}}
                
            # Process refund if paid and razorpay is configured
            if order['status'] in ['paid', 'shipped'] and order['razorpay_payment_id']:
                if has_razorpay_keys:
                    try:
                        razorpay_client.payment.refund(order['razorpay_payment_id'], {
                            "amount": int(float(order['total_amount']) * 100)
                        })
                    except Exception as e:
                        print("Refund error:", e)
                        return {'status': 500, 'data': {'message': 'Refund processing failed'}}
            
            # Update status and reason
            cursor.execute("UPDATE orders SET status = 'cancelled', cancel_reason = %s WHERE id = %s", (reason, order_id))
            conn.commit()
            
            return {'status': 200, 'data': {'message': 'Order cancelled and refund initiated successfully'}}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': {'message': 'Database error during cancellation'}}
    finally:
        conn.close()
