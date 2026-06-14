"""
PythonAnywhere WSGI Configuration File
Copy this content to your WSGI configuration file on PythonAnywhere

Path will be something like: /var/www/username_pythonanywhere_com_wsgi.py
Replace YOUR_USERNAME with your actual PythonAnywhere username
"""

# +++++++++++ FLASK +++++++++++
import sys
import os

# Add your project directory to the sys.path
# IMPORTANT: Replace YOUR_USERNAME with your actual PythonAnywhere username
project_home = '/home/YOUR_USERNAME/nursery_app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'a8f5f167f44f4964e6c998dee827110c3fcde9b8f3e1c8e5a5b5f5e5f5e5f5e5'
os.environ['DB_HOST'] = '34.10.117.44'
os.environ['DB_USER'] = 'root'
os.environ['DB_PASSWORD'] = 'Admin@123'
os.environ['DB_NAME'] = 'nursery_db'
os.environ['DB_PORT'] = '3306'

# Optional: Add these if you have Razorpay and email configured
# os.environ['RAZORPAY_KEY_ID'] = 'your_razorpay_key_id'
# os.environ['RAZORPAY_KEY_SECRET'] = 'your_razorpay_secret'
# os.environ['MAIL_SERVER'] = 'smtp.gmail.com'
# os.environ['MAIL_PORT'] = '587'
# os.environ['MAIL_USE_TLS'] = 'True'
# os.environ['MAIL_USERNAME'] = 'your_email@gmail.com'
# os.environ['MAIL_PASSWORD'] = 'your_app_password'

# Import Flask app
from wsgi import app as application

# For debugging (comment out in production)
# application.debug = False
