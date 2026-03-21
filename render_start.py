import subprocess
import sys
import os

def run_command(cmd, description):
    """Execute command and show description"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}...")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ {description} FAILED")
        sys.exit(1)
    
    print(f"\n✅ {description} succeeded")

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = os.getenv('PORT', '8000')
    
    # Run migrations
    run_command(
        "python manage.py migrate --noinput",
        "Running database migrations"
    )
    
    # Collect static files
    run_command(
        "python manage.py collectstatic --noinput",
        "Collecting static files"
    )
    
    # Create users
    run_command(
        "python crear_usuarios.py",
        "Creating default users"
    )
    
    # Start Gunicorn
    print(f"\n{'='*60}")
    print("🚀 Starting Gunicorn server...")
    print(f"{'='*60}\n")
    
    gunicorn_cmd = f"gunicorn --bind 0.0.0.0:{port} --workers 4 --worker-class sync SGIEVpy.wsgi:application"
    subprocess.run(gunicorn_cmd, shell=True)
