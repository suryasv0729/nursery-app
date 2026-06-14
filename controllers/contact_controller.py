import os
from utils.db import get_db_connection
from utils.mail import send_email

def submit_contact(data):
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return False

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                (data['name'], data['email'], data.get('subject', ''), data['message'])
            )
            conn.commit()
            
            # Send confirmation email to user
            send_email(
                to=data['email'],
                subject="We received your message!",
                body=f"Hi {data['name']},\n\nThank you for reaching out to us. We have received your message regarding '{data.get('subject', '')}' and will get back to you shortly.\n\nBest,\nNursery Team"
            )
            
            # Send real-time notification to the Admin Inbox
            admin_email = os.getenv('MAIL_USERNAME', 'admin@nursery.com')
            send_email(
                to=admin_email,
                subject=f"NEW CUSTOMER MESSAGE: {data.get('subject', 'General Inquiry')}",
                body=f"You have a new message from {data['name']} ({data['email']}):\n\n{data['message']}\n\nPlease reply to them directly."
            )
            
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def get_all_messages():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
            return cursor.fetchall()
    except Exception as e:
        print(e)
        return []
    finally:
        conn.close()
