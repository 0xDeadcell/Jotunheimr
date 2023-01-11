import os

# Secret key for secure sessions
SECRET_KEY = os.environ.get('SECRET_KEY')

# File upload settings
UPLOAD_FOLDER = 'assets/'
ALLOWED_EXTENSIONS = {'py'}

# Database connection settings
# DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jotunheimr.db'

# Server settings
PORT = os.environ.get('PORT', 80)
DEBUG = os.environ.get('DEBUG', True)
TESTING = os.environ.get('TESTING', True)