# 🚀 Quick Deployment Guide - GreenHaven Nursery

## ⚡ Quick Start (5 Minutes)

### Step 1: Authorize Your IP in Google Cloud SQL

1. Go to [Google Cloud Console](https://console.cloud.google.com/sql)
2. Select your instance: `free-trial-first-project`
3. Click on **"Connections"** tab
4. Under **"Authorized networks"**, click **"Add network"**
5. Add your current IP address (Google can detect it automatically)
6. Click **"Save"**

### Step 2: Test Database Connection

```bash
cd nursery_app

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test connection
python test_cloud_connection.py
```

### Step 3: Initialize Database Schema

```bash
# This creates all tables and the admin user
python init_cloud_db.py
```

When prompted, type `yes` to confirm.

### Step 4: Run the App Locally (Testing)

```bash
python app.py
```

Visit: **http://localhost:5000**

🎉 **You're done!** The app is now connected to Google Cloud SQL.

---

## 🌐 Deploy to Production

### Option A: Google Cloud Run (Recommended - 2 minutes)

**Why Cloud Run?**
- ✅ Easiest deployment
- ✅ Auto-scaling (0 to N instances)
- ✅ Pay only for actual usage
- ✅ HTTPS included
- ✅ No server management

**Deploy in one command:**

```bash
# First, build and submit
gcloud builds submit --tag gcr.io/project-cde250c9-df9f-459a-b29/nursery-app

# Then deploy
gcloud run deploy nursery-app \
  --image gcr.io/project-cde250c9-df9f-459a-b29/nursery-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "FLASK_ENV=production,DB_HOST=34.10.117.44,DB_USER=root,DB_PASSWORD=Admin@123,DB_NAME=nursery_db,DB_PORT=3306,SECRET_KEY=super_secret_dev_key"
```

**Your app will be live at:** `https://nursery-app-xxxxx-uc.a.run.app`

---

### Option B: Google App Engine (3 minutes)

**Why App Engine?**
- ✅ Simple configuration
- ✅ Built-in traffic splitting
- ✅ Integrated with other GCP services

```bash
gcloud app deploy app.yaml
```

**Your app will be live at:** `https://project-cde250c9-df9f-459a-b29.appspot.com`

---

### Option C: Google Compute Engine (VM) - 10 minutes

**Why Compute Engine?**
- ✅ Full control over environment
- ✅ Can run additional services
- ✅ Cost-effective for consistent traffic

See `DEPLOYMENT_GUIDE.md` for detailed VM setup instructions.

---

## 🔐 Security Improvements (Recommended)

### 1. Use Google Secret Manager

Instead of hardcoding passwords, store them securely:

```bash
# Store database password
echo -n "Admin@123" | gcloud secrets create db-password --data-file=-

# Store Flask secret key
python -c "import secrets; print(secrets.token_hex(32))" > /tmp/secret.txt
gcloud secrets create flask-secret-key --data-file=/tmp/secret.txt
rm /tmp/secret.txt
```

Then deploy Cloud Run with secrets:

```bash
gcloud run deploy nursery-app \
  --image gcr.io/project-cde250c9-df9f-459a-b29/nursery-app \
  --set-secrets "DB_PASSWORD=db-password:latest,SECRET_KEY=flask-secret-key:latest" \
  --set-env-vars "FLASK_ENV=production,DB_HOST=34.10.117.44,DB_USER=root,DB_NAME=nursery_db,DB_PORT=3306"
```

### 2. Use Cloud SQL Proxy (Best Practice)

Instead of public IP, use secure proxy:

**Local development:**
```bash
# Download Cloud SQL Proxy
# Windows: https://dl.google.com/cloudsql/cloud_sql_proxy_x64.exe

# Run proxy (in separate terminal)
cloud_sql_proxy.exe -instances=project-cde250c9-df9f-459a-b29:us-central1:free-trial-first-project=tcp:3306

# Update .env
DB_HOST=127.0.0.1
```

**For Cloud Run:**
```bash
gcloud run deploy nursery-app \
  --add-cloudsql-instances project-cde250c9-df9f-459a-b29:us-central1:free-trial-first-project \
  --set-env-vars "DB_HOST=/cloudsql/project-cde250c9-df9f-459a-b29:us-central1:free-trial-first-project"
```

---

## 📊 Monitoring Your App

### View Logs

**Cloud Run:**
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50 --format json
```

**App Engine:**
```bash
gcloud app logs tail -s default
```

### Check Service Status

```bash
# Cloud Run
gcloud run services describe nursery-app --region us-central1

# App Engine  
gcloud app describe
```

---

## 🔄 Updating Your App

### Update and Redeploy

**Cloud Run:**
```bash
# After making changes
gcloud builds submit --tag gcr.io/project-cde250c9-df9f-459a-b29/nursery-app
gcloud run deploy nursery-app --image gcr.io/project-cde250c9-df9f-459a-b29/nursery-app
```

**App Engine:**
```bash
gcloud app deploy
```

---

## 🧪 Testing Checklist

Before going to production, test:

- [ ] User registration works
- [ ] User login works  
- [ ] Admin login works (admin@nursery.com / admin123)
- [ ] Products are displayed
- [ ] Add to cart works
- [ ] Checkout process works
- [ ] Order history shows orders
- [ ] Contact form sends messages
- [ ] All images load correctly

---

## 💰 Cost Estimate

**Monthly costs for low to medium traffic:**

| Service | Cost |
|---------|------|
| Cloud SQL (db-f1-micro) | $10-15 |
| Cloud Run | $0-10 (generous free tier) |
| Storage & Bandwidth | $1-5 |
| **Total** | **$11-30/month** |

**Free tier includes:**
- Cloud Run: 2 million requests/month free
- Cloud SQL: Some hours free per month
- 1 GB network egress free

---

## 🆘 Common Issues & Solutions

### Issue: "Connection refused" or "Can't connect to MySQL"

**Solution:**
1. Check if Cloud SQL instance is running
2. Verify your IP is authorized:
   - Console → SQL → Connections → Authorized networks
3. Test with MySQL client:
   ```bash
   mysql -h 34.10.117.44 -u root -p nursery_db
   ```

### Issue: "Access denied for user"

**Solution:**
- Verify password in `.env` file matches Cloud SQL
- Check username is correct (`root`)
- Ensure database `nursery_db` exists

### Issue: "No module named 'pymysql'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Tables not found

**Solution:**
```bash
python init_cloud_db.py
```

### Issue: Static files (CSS/JS/Images) not loading

**Solution:**
- For Cloud Run/App Engine: Files are served by Flask
- Check file paths in templates are correct
- Verify files exist in `static/` directory

---

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| FLASK_ENV | Yes | development | Set to `production` for deployment |
| SECRET_KEY | Yes | - | Flask secret key for sessions |
| DB_HOST | Yes | - | Cloud SQL public IP: `34.10.117.44` |
| DB_USER | Yes | - | Database username: `root` |
| DB_PASSWORD | Yes | - | Database password |
| DB_NAME | Yes | - | Database name: `nursery_db` |
| DB_PORT | No | 3306 | MySQL port |
| MAIL_USERNAME | No | - | Gmail for sending emails |
| MAIL_PASSWORD | No | - | Gmail app password |
| RAZORPAY_KEY_ID | No | - | Razorpay API key |
| RAZORPAY_KEY_SECRET | No | - | Razorpay secret |

---

## 📚 Additional Resources

- **Full Deployment Guide:** See `DEPLOYMENT_GUIDE.md`
- **Google Cloud Documentation:** https://cloud.google.com/docs
- **Cloud Run Docs:** https://cloud.google.com/run/docs
- **Cloud SQL Docs:** https://cloud.google.com/sql/docs
- **Support:** File an issue or check logs

---

## 🎯 Next Steps After Deployment

1. ✅ Test all features
2. 🔐 Update SECRET_KEY with a strong random value
3. 📧 Configure email settings (MAIL_USERNAME, MAIL_PASSWORD)
4. 💳 Add Razorpay credentials for payments
5. 🌐 Configure custom domain (optional)
6. 📊 Set up monitoring and alerts
7. 🔒 Enable HTTPS (automatic with Cloud Run/App Engine)
8. 🚀 Share your nursery store with the world!

---

**Happy Deploying! 🌱🚀**

For detailed instructions, see `DEPLOYMENT_GUIDE.md`
