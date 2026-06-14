# 🚀 Render.com Deployment Guide

## Step-by-Step Instructions

---

## ✅ Step 1: Push Code to GitHub

Your code is ready! Now push it to GitHub:

1. **Create a new repository on GitHub:**
   - Go to [github.com](https://github.com)
   - Click the "+" icon → "New repository"
   - Name: `nursery-app` (or any name you like)
   - Make it **Public**
   - **DON'T** initialize with README
   - Click "Create repository"

2. **Push your code:**
   
   Open Command Prompt in your project folder and run:

   ```bash
   cd c:\Users\DELL\Downloads\Kanna\Kanna\nursery_app
   
   git branch -M main
   
   git remote add origin https://github.com/YOUR_USERNAME/nursery-app.git
   
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your GitHub username!

---

## 🌐 Step 2: Deploy on Render

1. **Go to [Render.com](https://render.com)**

2. **Sign up / Sign in with GitHub**
   - Click "Get Started for Free"
   - Choose "Sign in with GitHub"
   - Authorize Render to access your repositories

3. **Create a New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect to your `nursery-app` repository
   - Click "Connect"

4. **Configure the service:**

   Fill in these details:

   - **Name**: `nursery-app` (or any name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn -b :$PORT wsgi:app --timeout 300 --workers 2
     ```
   - **Instance Type**: `Free`

5. **Add Environment Variables:**

   Click "Advanced" → "Add Environment Variable"

   Add these one by one:

   ```
   FLASK_ENV=production
   SECRET_KEY=a8f5f167f44f4964e6c998dee827110c3fcde9b8f3e1c8e5a5b5f5e5f5e5f5e5
   DB_HOST=34.10.117.44
   DB_USER=root
   DB_PASSWORD=Admin@123
   DB_NAME=nursery_db
   DB_PORT=3306
   ```

6. **Click "Create Web Service"**

   Render will now:
   - Build your app (takes 3-5 minutes)
   - Deploy it
   - Give you a URL like: `https://nursery-app.onrender.com`

---

## 🗄️ Step 3: Configure Database Access

1. **Go to [Google Cloud Console](https://console.cloud.google.com/sql)**

2. Click your SQL instance: **"free-trial-first-project"**

3. Click **"Connections"** tab

4. Under **"Authorized networks"**, click **"Add network"**

5. Add:
   - **Name**: `Render`
   - **Network**: `0.0.0.0/0`

6. Click **"Done"** then **"Save"**

---

## 🔨 Step 4: Initialize Database

Once your Render app is deployed:

1. Go to your Render dashboard
2. Click on your service
3. Click **"Shell"** tab (on the left)
4. Run this command:

```bash
python init_cloud_db.py
```

This creates all database tables.

---

## 🎉 Step 5: Visit Your App!

Your app is now live at: **`https://nursery-app.onrender.com`**

(Replace with your actual Render URL)

---

## ⚠️ Important Notes

### Free Tier Limitations:

✅ **Included:**
- Free hosting forever
- HTTPS included
- 750 hours/month
- Auto-deploy from GitHub

⚠️ **Limitations:**
- **App sleeps after 15 minutes of inactivity**
- First request after sleep takes 30-60 seconds
- 512 MB RAM

### Keeping App Awake (Optional):

Use a free service like [UptimeRobot](https://uptimerobot.com) to ping your app every 5 minutes.

---

## 🔄 Updating Your App

Whenever you make changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your change description"
   git push
   ```

2. Render automatically redeploys! (takes 2-3 minutes)

---

## 🐛 Troubleshooting

### Check Logs:
- Go to Render dashboard
- Click your service
- Click "Logs" tab
- Look for errors

### Common Issues:

**Build Failed:**
- Check `requirements.txt` is correct
- Verify Python version compatibility

**Database Connection Failed:**
- Check Google Cloud SQL authorized networks
- Verify environment variables are correct

**App Not Loading:**
- Check logs for specific error
- Verify `wsgi.py` exists and is correct

---

## 📞 Support

- Render Docs: [https://render.com/docs](https://render.com/docs)
- Render Community: [https://community.render.com](https://community.render.com)

---

**You're all set! Your nursery app will be live in minutes! 🌱🎉**
