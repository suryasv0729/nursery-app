@echo off
echo ========================================
echo  GreenHaven Nursery - Cloud Deployment
echo ========================================
echo.

echo Step 1: Setting up Google Cloud project...
call gcloud config set project project-cde250c9-df9f-459a-b29
if errorlevel 1 (
    echo ERROR: Failed to set project. Make sure gcloud is installed and authenticated.
    echo Run: gcloud auth login
    pause
    exit /b 1
)
echo.

echo Step 2: Enabling required APIs...
echo This may take a minute...
call gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com
if errorlevel 1 (
    echo ERROR: Failed to enable APIs
    pause
    exit /b 1
)
echo.

echo Step 3: Building Docker image...
echo This may take 2-5 minutes... Please wait...
call gcloud builds submit --tag gcr.io/project-cde250c9-df9f-459a-b29/nursery-app
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)
echo.

echo Step 4: Deploying to Cloud Run...
call gcloud run deploy nursery-app ^
  --image gcr.io/project-cde250c9-df9f-459a-b29/nursery-app ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --memory 512Mi ^
  --cpu 1 ^
  --add-cloudsql-instances project-cde250c9-df9f-459a-b29:us-central1:free-trial-first-project ^
  --set-env-vars "FLASK_ENV=production,DB_HOST=34.10.117.44,DB_USER=root,DB_PASSWORD=Admin@123,DB_NAME=nursery_db,DB_PORT=3306,SECRET_KEY=super_secret_dev_key"

if errorlevel 1 (
    echo ERROR: Deployment failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo  Getting your app URL...
echo ========================================
call gcloud run services describe nursery-app --region us-central1 --format "value(status.url)"
echo.

echo ========================================
echo  Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open the URL shown above in your browser
echo 2. Test the app features
echo 3. Login as admin: admin@nursery.com / admin123
echo 4. IMPORTANT: Update SECRET_KEY for production security
echo.
echo To view logs:
echo   gcloud logging tail "resource.type=cloud_run_revision"
echo.
echo To update the app:
echo   gcloud builds submit --tag gcr.io/project-cde250c9-df9f-459a-b29/nursery-app
echo   gcloud run deploy nursery-app --image gcr.io/project-cde250c9-df9f-459a-b29/nursery-app --region us-central1
echo.
pause
