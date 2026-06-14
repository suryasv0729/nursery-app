# GreenHaven Nursery - Deployment Guide

## 🌐 Google Cloud SQL Configuration

Your database is already set up with these credentials:
- **Instance Connection Name**: `project-cde250c9-df9f-459a-b29:us-central1:free-trial-first-project`
- **Public IP**: `34.10.117.44`
- **Database Name**: `nursery_db`
- **Username**: `root`
- **Password**: `Admin@123`
- **Port**: `3306`

---

## 📋 Pre-Deployment Steps

### 1. Initialize Database Schema

First, you need to create the database schema in your Google Cloud SQL instance:

```bash
# Install MySQL client if not already installed
# Windows: Download from https://dev.mysql.com/downloads/mysql/
# Or use MySQL Workbench

# Connect to your Cloud SQL instance
mysql -h 34.10.117.44 -u root -p

# Enter password: Admin@123

# Then run the schema file
source schema.sql

# Or copy-paste the contents of schema.sql
```

**Alternative: Use Cloud SQL Studio from Google Cloud Console**
1. Go to Google Cloud Console → SQL → Your Instance
2. Click "Cloud SQL Studio" or "Import"
3. Upload and run `schema.sql`

### 2. Configure Google Cloud SQL Instance

Ensure your Cloud SQL instance allows connections:

1. Go to Google Cloud Console → SQL → Your Instance
2. Click "Connections" tab
3. Under "Authorized networks", add:
   - Your local IP (for testing)
   - `0.0.0.0/0` (for public access - **not recommended for production**)
   - Or configure Cloud SQL Proxy (recommended)

---

## 🚀 Deployment Options

### Option 1: Google App Engine (Easiest)

**Prerequisites:**
- Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- Authenticate: `gcloud auth login`
- Set project: `gcloud config set project project-cde250c9-df9f-459a-b29`

**Deploy:**
```bash
cd nursery_app
gcloud app deploy app.yaml
```

**Access your app:**
```bash
gcloud app browse
```

---

### Option 2: Google Cloud Run (Recommended)

**Prerequisites:**
- Install Docker Desktop
- Install Google Cloud SDK

**Steps:**

1. **Enable required APIs:**
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

2. **Build and push Docker image:**
```bash
cd nursery_app

# Build the image
gcloud builds submit --tag gcr.io/project-cde250c9-df9f-459a-b29/nursery-app

# Or build locally and push
docker build -t gcr.io/project-cde250c9-df9f-459a-b29/nursery-app .
docker push gcr.io/project-cde250c9-df9f-459a-b29/nursery-app
```

3. **Deploy to Cloud Run:**
```bash
gcloud run deploy nursery-app \
  --image gcr.io/project-cde250c9-df9f-459a-b29/nursery-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "FLASK_ENV=production,DB_HOST=34.10.117.44,DB_USER=root,DB_PASSWORD=Admin@123,DB_NAME=nursery_db,DB_PORT=3306,SECRET_KEY=super_secret_dev_key" \
  --memory 512Mi \
  --cpu 1
```

**Note:** For better security, use Secret Manager instead of passing credentials directly:
```bash
# Create secrets
echo -n "Admin@123" | gcloud secrets create db-password --data-file=-

# Deploy with secret
gcloud run deploy nursery-app \
  --image gcr.io/project-cde250c9-df9f-459a-b29/nursery-app \
  --set-secrets DB_PASSWORD=db-password:latest
```

---

### Option 3: Google Compute Engine (VM)

**Steps:**

1. **Create a VM instance:**
```bash
gcloud compute instances create nursery-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --tags=http-server,https-server
```

2. **SSH into the instance:**
```bash
gcloud compute ssh nursery-vm --zone=us-central1-a
```

3. **Install dependencies on the VM:**
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3-pip python3-venv nginx

# Install MySQL client
sudo apt-get install -y default-libmysqlclient-dev pkg-config

# Clone or upload your app
# If using git:
# git clone <your-repo-url>
# cd nursery_app

# Or upload via scp:
# From local machine:
# gcloud compute scp --recurse ./nursery_app nursery-vm:~/ --zone=us-central1-a
```

4. **Set up the application:**
```bash
cd nursery_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Test the connection
python3 -c "from utils.db import get_db_connection; conn = get_db_connection(); print('Connected successfully!')"
```

5. **Run with Gunicorn:**
```bash
# Test run
gunicorn --bind 0.0.0.0:8080 wsgi:app

# For production, create a systemd service
sudo nano /etc/systemd/system/nursery-app.service
```

Add this content:
```ini
[Unit]
Description=Nursery Flask App
After=network.target

[Service]
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/nursery_app
Environment="PATH=/home/YOUR_USERNAME/nursery_app/venv/bin"
ExecStart=/home/YOUR_USERNAME/nursery_app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 wsgi:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable nursery-app
sudo systemctl start nursery-app
sudo systemctl status nursery-app
```

6. **Configure Nginx as reverse proxy:**
```bash
sudo nano /etc/nginx/sites-available/nursery-app
```

Add:
```nginx
server {
    listen 80;
    server_name YOUR_EXTERNAL_IP;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/YOUR_USERNAME/nursery_app/static;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/nursery-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Open firewall:**
```bash
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags http-server

gcloud compute firewall-rules create allow-https \
  --allow tcp:443 \
  --target-tags https-server
```

---

## 🔒 Security Best Practices

### 1. Update Environment Variables
**Never commit `.env` file to Git!**

Create `.env.production`:
```env
FLASK_ENV=production
SECRET_KEY=GENERATE_NEW_STRONG_SECRET_KEY_HERE
DB_HOST=34.10.117.44
DB_USER=root
DB_PASSWORD=Admin@123
DB_NAME=nursery_db
DB_PORT=3306
```

Generate a strong secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### 2. Use Google Secret Manager
```bash
# Store secrets
echo -n "your-secret-key" | gcloud secrets create flask-secret-key --data-file=-
echo -n "Admin@123" | gcloud secrets create db-password --data-file=-
```

### 3. Restrict Database Access
- Remove `0.0.0.0/0` from authorized networks
- Only allow your App Engine/Cloud Run/Compute Engine IPs
- Or use Cloud SQL Proxy (best practice)

### 4. Use Cloud SQL Proxy (Recommended)

**For local development:**
```bash
# Download Cloud SQL Proxy
# Windows: https://dl.google.com/cloudsql/cloud_sql_proxy_x64.exe

# Run proxy
cloud_sql_proxy.exe -instances=project-cde250c9-df9f-459a-b29:us-central1:free-trial-first-project=tcp:3306

# Update .env
DB_HOST=127.0.0.1
```

---

## 🧪 Testing the Connection

### Test Database Connection:
```bash
cd nursery_app
python3 -c "from utils.db import get_db_connection; conn = get_db_connection(); cursor = conn.cursor(); cursor.execute('SELECT VERSION()'); print('MySQL Version:', cursor.fetchone()); conn.close()"
```

### Test Flask App Locally:
```bash
# Activate virtual environment (if not already)
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py
```

Visit: `http://localhost:5000`

---

## 📊 Monitoring & Logs

### View logs:

**App Engine:**
```bash
gcloud app logs tail -s default
```

**Cloud Run:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=nursery-app" --limit 50
```

**Compute Engine:**
```bash
# SSH into VM
gcloud compute ssh nursery-vm --zone=us-central1-a

# View logs
sudo journalctl -u nursery-app -f
```

---

## 🔄 Continuous Deployment

### Option 1: Using Cloud Build
Create `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/nursery-app', '.']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/nursery-app']
  
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'nursery-app'
      - '--image=gcr.io/$PROJECT_ID/nursery-app'
      - '--region=us-central1'
      - '--platform=managed'
```

Connect to GitHub:
```bash
gcloud builds triggers create github \
  --repo-name=YOUR_REPO \
  --repo-owner=YOUR_USERNAME \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

---

## 🆘 Troubleshooting

### Connection Issues:
1. Check Cloud SQL instance is running
2. Verify authorized networks include your IP
3. Test with MySQL client directly
4. Check firewall rules

### Application Errors:
1. Check application logs
2. Verify environment variables are set correctly
3. Ensure database schema is initialized
4. Check Python dependencies are installed

### Performance Issues:
1. Monitor Cloud SQL metrics
2. Add database indexes
3. Increase instance resources
4. Enable connection pooling

---

## 📝 Next Steps

1. ✅ Initialize database schema in Cloud SQL
2. ✅ Choose a deployment option (Cloud Run recommended)
3. ✅ Deploy the application
4. ⚠️ Update SECRET_KEY in production
5. 🔒 Configure Cloud SQL Proxy or restrict network access
6. 📧 Update MAIL_USERNAME and MAIL_PASSWORD for emails
7. 💳 Update Razorpay credentials for payments
8. 🌐 Configure custom domain (optional)
9. 🔐 Set up SSL certificate
10. 📊 Set up monitoring and alerts

---

## 🌐 Custom Domain (Optional)

1. Register domain or use existing
2. Add DNS records pointing to your app
3. Map domain in Google Cloud:

**For App Engine:**
```bash
gcloud app domain-mappings create yourdomain.com
```

**For Cloud Run:**
```bash
gcloud beta run domain-mappings create --service nursery-app --domain yourdomain.com --region us-central1
```

---

## 💰 Cost Estimation

**Free Tier Eligible:**
- Cloud SQL: Limited hours free per month
- Cloud Run: 2 million requests free
- App Engine: 28 instance hours/day free

**Typical Monthly Costs (Low Traffic):**
- Cloud SQL (db-f1-micro): ~$10-15/month
- Cloud Run: ~$5-10/month
- App Engine: ~$5-20/month
- Compute Engine (e2-micro): ~$7/month (eligible for free tier)

---

## 📚 Additional Resources

- [Google Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [App Engine Documentation](https://cloud.google.com/appengine/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)

---

**Good luck with your deployment! 🚀🌱**
