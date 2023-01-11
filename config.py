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
TEMPLATES_AUTO_RELOAD = os.environ.get('TEMPLATES_AUTO_RELOAD', True)
SEND_FILE_MAX_AGE_DEFAULT = os.environ.get('SEND_FILE_MAX_AGE_DEFAULT', 0)