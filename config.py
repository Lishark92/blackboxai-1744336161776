import os

# File upload configurations
UPLOAD_FOLDER = 'static/uploads'
GENERATED_FOLDER = 'static/generated'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Flask configurations
SECRET_KEY = 'your-secret-key-here'  # Change this in production
DEBUG = True

# Create upload and generated folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
