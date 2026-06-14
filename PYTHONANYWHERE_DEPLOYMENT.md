# 🐍 Complete PythonAnywhere Deployment Guide

## Step-by-Step Instructions for Your Nursery App

---

## 📋 PART 1: Sign Up & Initial Setup

### Step 1: Create PythonAnywhere Account

1. Go to **[https://www.pythonanywhere.com](https://www.pythonanywhere.com)**
2. Click **"Start running Python online"** or **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Fill in:
   - Username (this will be in your URL: `username.pythonanywhere.com`)
   - Email
   - Password
5. Verify your email
6. Log in to your dashboard

---

## 📁 PART 2: Upload Your Application

### Step 2: Open Bash Console

1. From PythonAnywhere dashboard, click **"Consoles"** tab
2. Click **"Bash"** to open a new bash console
3. You'll see a terminal like: `username ~ $`

### Step 3: Upload Your Files

**Option A: Using Zip Upload (Easiest)**

1. On your local computer, compress the `nursery_app` folder to a ZIP file
2. In PythonAnywhere, click **"Files"** tab
3. Click **"Upload a file"**
4. Upload your `nursery_app.zip`
5. Go back to **Bash console** and run:
```bash
cd ~
unzip nursery_app.zip
cd nursery_app
ls  # Verify files are there
```

**Option B: Using Git (Recommended for updates)**

1. First, create a GitHub repository with your code
2. In PythonAnywhere Bash console:
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git nursery_app
cd nursery_app
ls  # Verify files are there
```

---

## 🔧 PART 3: Set Up Virtual Environment

### Step 4: Create Virtual Environment

In the Bash console, run these commands:

```bash
cd ~/nursery_app

# Create virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 nursery_env

# You should see (nursery_env) before your prompt now
# If not, activate it manually:
workon nursery_env
```

### Step 5: Install Dependencies

```bash
# Make sure you're in the virtual environment (you should see (nursery_env))
cd ~/nursery_app

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages:**
- Flask
- PyMySQL
- PyJWT
- Werkzeug
- razorpay
- Flask-Mail
- python-dotenv
- cryptography
- gunicorn

---

## 🌐 PART 4: Configure Web App

### Step 6: Create Web App

1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Click **"Next"** (for your free domain: `username.pythonanywhere.com`)
4. Select **"Manual configuration"** (NOT Flask)
5. Select **"Python 3.10"**
6. Click **"Next"**

### Step 7: Configure WSGI File

1. On the **Web** tab, scroll to **"Code"** section
2. Click on the **WSGI configuration file** link (it will be something like `/var/www/username_pythonanywhere_com_wsgi.py`)
3. **Delete all the existing content** in the file
4. **Copy and paste this configuration:**

```python
# +++++++++++ FLASK +++++++++++
import sys
import os

# Add your project directory to the sys.path
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

# Import Flask app
from wsgi import app as application
```

5. **Replace `YOUR_USERNAME`** with your actual PythonAnywhere username
6. Click **"Save"** (top right corner)

### Step 8: Configure Virtual Environment Path

1. Still on the **Web** tab, scroll to **"Virtualenv"** section
2. Click **"Enter path to a virtualenv"**
3. Enter: `/home/YOUR_USERNAME/.virtualenvs/nursery_env`
4. Replace `YOUR_USERNAME` with your actual username
5. Click the checkmark ✓

### Step 9: Configure Static Files

1. Scroll to **"Static files"** section
2. Click **"Enter URL"** and add:
   - **URL:** `/static/`
   - **Directory:** `/home/YOUR_USERNAME/nursery_app/static`
3. Replace `YOUR_USERNAME` with your actual username

---

## 🗄️ PART 5: Database Configuration

### Step 10: Allow PythonAnywhere IP in Google Cloud SQL

**Important:** Your Google Cloud SQL must allow connections from PythonAnywhere.

1. Go to **[Google Cloud Console](https://console.cloud.google.com/sql)**
2. Click your SQL instance: `free-trial-first-project`
3. Click **"Connections"** tab
4. Under **"Authorized networks"**, click **"Add network"**
5. Add PythonAnywhere IP ranges:
   - **Name:** `PythonAnywhere`
   - **Network:** `0.0.0.0/0` (allows all IPs - not recommended for production)
   
   **For better security**, add only PythonAnywhere's specific IPs (see PythonAnywhere documentation)

6. Click **"Save"**

### Step 11: Test Database Connection

In the Bash console:

```bash
workon nursery_env
cd ~/nursery_app

# Test connection
python3 << EOF
import pymysql
try:
    conn = pymysql.connect(
        host='34.10.117.44',
        user='root',
        password='Admin@123',
        database='nursery_db',
        port=3306
    )
    print("✅ Database connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
EOF
```

If connection fails, check:
- Google Cloud SQL authorized networks
- Database credentials are correct
- Cloud SQL instance is running

---

## ✅ PART 6: Initialize Database Schema

### Step 12: Create Database Tables

In the Bash console:

```bash
workon nursery_env
cd ~/nursery_app

# Run initialization script
python3 init_cloud_db.py
```

**Or manually run schema.sql:**

```bash
# Install mysql client
pip install mysqlclient

# Run schema
mysql -h 34.10.117.44 -u root -pAdmin@123 nursery_db < schema.sql
```

---

## 🚀 PART 7: Launch Your App

### Step 13: Reload Web App

1. Go back to the **Web** tab
2. Scroll to the top
3. Click the big green **"Reload username.pythonanywhere.com"** button
4. Wait for it to finish (you'll see "All done!")

### Step 14: Open Your App

1. Click on your URL: **`https://username.pythonanywhere.com`**
2. Your nursery app should now be live! 🎉

---

## 🐛 PART 8: Troubleshooting

### Check Error Logs

If your app doesn't load, check the logs:

1. On the **Web** tab, scroll to **"Log files"** section
2. Click on **"Error log"**
3. Look for error messages

**Common errors and fixes:**

#### Error: "ImportError: No module named 'flask'"
**Fix:** Virtual environment not activated or dependencies not installed
```bash
workon nursery_env
pip install -r requirements.txt
```

#### Error: "Can't connect to MySQL server"
**Fix:** Database connection issue
- Check Google Cloud SQL authorized networks
- Verify credentials in WSGI file
- Ensure Cloud SQL instance is running

#### Error: "No such file or directory"
**Fix:** Wrong path in WSGI file
- Verify your username in the paths
- Check files are uploaded correctly

#### Error: "500 Internal Server Error"
**Fix:** Check error log for specific issue
```bash
tail -f /var/log/username.pythonanywhere.com.error.log
```

---

## 🔄 PART 9: Updating Your App

### To Update Code:

**If using Git:**
```bash
cd ~/nursery_app
git pull origin main
```

**If using upload:**
1. Upload new files via Files tab
2. Replace old files

### After updating, always reload:
1. Go to **Web** tab
2. Click **"Reload"** button

---

## ⚙️ PART 10: Advanced Configuration

### Setting Up Custom Domain (Paid Feature)

PythonAnywhere free tier uses: `username.pythonanywhere.com`

For custom domain (e.g., `mynursery.com`), upgrade to paid plan.

### Enable HTTPS

PythonAnywhere automatically provides HTTPS for all apps! 🔒

Your app will be accessible at: `https://username.pythonanywhere.com`

---

## 📊 PART 11: Free Tier Limits

PythonAnywhere Free Account includes:

✅ **Included:**
- 1 web app at `username.pythonanywhere.com`
- 512 MB disk space
- HTTPS included
- Daily CPU quota: 100 seconds
- 1 bash console
- MySQL database (local only - you're using external Google Cloud SQL)

❌ **Not Included:**
- Custom domains
- SSH access
- Always-on tasks
- Multiple web apps
- Internet access from code (for API calls)

⚠️ **Important for your app:**
- **Payment gateway API calls** (Razorpay) need "Internet access" which requires paid plan
- **Email sending** might be restricted on free tier
- Consider upgrading to $5/month plan if you need these features

---

## 💡 Quick Reference

### Useful Commands:

```bash
# Activate virtual environment
workon nursery_env

# Check what's installed
pip list

# View logs
tail -f /var/log/username.pythonanywhere.com.error.log

# Test database connection
python3 -c "import pymysql; conn = pymysql.connect(host='34.10.117.44', user='root', password='Admin@123', database='nursery_db'); print('Connected!'); conn.close()"

# Restart console if needed
# Just close and open a new bash console
```

### Important URLs:

- **Dashboard:** `https://www.pythonanywhere.com/user/username/`
- **Your App:** `https://username.pythonanywhere.com`
- **Web Config:** `https://www.pythonanywhere.com/user/username/webapps/`
- **Files:** `https://www.pythonanywhere.com/user/username/files/`

---

## 📞 Getting Help

**PythonAnywhere Support:**
- Forums: [https://www.pythonanywhere.com/forums/](https://www.pythonanywhere.com/forums/)
- Help: [https://help.pythonanywhere.com](https://help.pythonanywhere.com)
- Email: support@pythonanywhere.com (for paid accounts)

**Common Issues:**
- [Database Connection Guide](https://help.pythonanywhere.com/pages/ExternalMySQL)
- [Flask Deployment Guide](https://help.pythonanywhere.com/pages/Flask/)
- [Debugging Web Apps](https://help.pythonanywhere.com/pages/DebuggingImportError/)

---

## ✅ Checklist

Before going live, make sure:

- [ ] Account created on PythonAnywhere
- [ ] Code uploaded to `~/nursery_app`
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Web app created (Manual configuration, Python 3.10)
- [ ] WSGI file configured with correct username and env variables
- [ ] Virtual environment path set in Web tab
- [ ] Static files path configured
- [ ] Google Cloud SQL authorized networks updated
- [ ] Database connection tested successfully
- [ ] Database schema initialized (`init_cloud_db.py` or `schema.sql`)
- [ ] Web app reloaded
- [ ] App tested and working at `username.pythonanywhere.com`

---

## 🎉 Success!

If everything is working, you should see your nursery app live at:

**`https://YOUR_USERNAME.pythonanywhere.com`**

Congratulations! 🌱🎊

---

## 📝 Notes

- **Free tier has daily CPU limits** - if you exceed them, your site will slow down until midnight UTC
- **No automatic backups** - backup your code and database regularly
- **Upload size limit:** 100 MB per file on free tier
- Consider upgrading to Hacker plan ($5/month) if you need:
  - Custom domain
  - More CPU
  - Scheduled tasks
  - API access from your code (for Razorpay, email sending, etc.)

