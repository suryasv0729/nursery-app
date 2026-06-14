"""
Interactive deployment helper script
Helps you deploy your Flask app to Google Cloud
"""
import os
import subprocess
import sys

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(command, description):
    """Run shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_gcloud():
    """Check if gcloud is installed"""
    try:
        subprocess.run(["gcloud", "version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print_header("GreenHaven Nursery - Deployment Helper")
    
    # Check prerequisites
    print("Checking prerequisites...")
    
    if not check_gcloud():
        print("\n❌ Google Cloud SDK not found!")
        print("\n📥 Please install it from: https://cloud.google.com/sdk/docs/install")
        print("After installation, run: gcloud init")
        sys.exit(1)
    
    print("✅ Google Cloud SDK found!\n")
    
    # Show deployment options
    print("Choose deployment target:\n")
    print("1. 🚀 Cloud Run (Recommended - Easiest & Auto-scaling)")
    print("2. 🌐 App Engine (Simple configuration)")
    print("3. 🧪 Test connection only")
    print("4. 📊 Initialize database")
    print("5. ❌ Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        deploy_cloud_run()
    elif choice == "2":
        deploy_app_engine()
    elif choice == "3":
        test_connection()
    elif choice == "4":
        initialize_database()
    elif choice == "5":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice!")
        sys.exit(1)

def deploy_cloud_run():
    """Deploy to Cloud Run"""
    print_header("Deploy to Cloud Run")
    
    project_id = "project-cde250c9-df9f-459a-b29"
    app_name = "nursery-app"
    region = "us-central1"
    
    print(f"Project ID: {project_id}")
    print(f"App Name: {app_name}")
    print(f"Region: {region}\n")
    
    confirm = input("Continue with deployment? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Deployment cancelled")
        return
    
    # Step 1: Build image
    print_header("Step 1/2: Building Docker Image")
    image_url = f"gcr.io/{project_id}/{app_name}"
    
    if not run_command(
        f"gcloud builds submit --tag {image_url}",
        "Building and uploading Docker image"
    ):
        print("\n❌ Build failed! Check errors above.")
        return
    
    # Step 2: Deploy to Cloud Run
    print_header("Step 2/2: Deploying to Cloud Run")
    
    deploy_cmd = f"""gcloud run deploy {app_name} \
--image {image_url} \
--platform managed \
--region {region} \
--allow-unauthenticated \
--memory 512Mi \
--cpu 1 \
--set-env-vars "FLASK_ENV=production,DB_HOST=34.10.117.44,DB_USER=root,DB_PASSWORD=Admin@123,DB_NAME=nursery_db,DB_PORT=3306,SECRET_KEY=super_secret_dev_key" """
    
    if run_command(deploy_cmd, "Deploying to Cloud Run"):
        print_header("🎉 Deployment Successful!")
        print("\n📝 Next steps:")
        print("1. Get your app URL:")
        print(f"   gcloud run services describe {app_name} --region {region} --format 'value(status.url)'")
        print("\n2. View logs:")
        print(f"   gcloud logging read 'resource.type=cloud_run_revision' --limit 50")
        print("\n3. Update deployment:")
        print(f"   gcloud builds submit --tag {image_url}")
        print(f"   gcloud run deploy {app_name} --image {image_url} --region {region}")
        
        # Try to get URL
        try:
            result = subprocess.run(
                f"gcloud run services describe {app_name} --region {region} --format 'value(status.url)'",
                shell=True, capture_output=True, text=True, check=True
            )
            url = result.stdout.strip()
            if url:
                print(f"\n🌐 Your app is live at: {url}")
        except:
            pass
    else:
        print("\n❌ Deployment failed! Check errors above.")

def deploy_app_engine():
    """Deploy to App Engine"""
    print_header("Deploy to App Engine")
    
    if not os.path.exists("app.yaml"):
        print("❌ app.yaml not found!")
        return
    
    print("This will deploy to Google App Engine")
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Deployment cancelled")
        return
    
    if run_command("gcloud app deploy app.yaml", "Deploying to App Engine"):
        print_header("🎉 Deployment Successful!")
        print("\n📝 Next steps:")
        print("1. Open your app: gcloud app browse")
        print("2. View logs: gcloud app logs tail -s default")
        print("3. Update: gcloud app deploy")

def test_connection():
    """Test database connection"""
    print_header("Test Database Connection")
    
    if not os.path.exists("test_cloud_connection.py"):
        print("❌ test_cloud_connection.py not found!")
        return
    
    run_command("python test_cloud_connection.py", "Testing connection")

def initialize_database():
    """Initialize database"""
    print_header("Initialize Database")
    
    if not os.path.exists("init_cloud_db.py"):
        print("❌ init_cloud_db.py not found!")
        return
    
    print("⚠️  This will create/reset database tables!")
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Operation cancelled")
        return
    
    run_command("python init_cloud_db.py", "Initializing database")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Deployment cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
