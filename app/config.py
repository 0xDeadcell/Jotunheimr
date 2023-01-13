import yaml
import os

# Secret key for secure sessions
SECRET_KEY = os.environ.get('SECRET_KEY')

# File upload settings
UPLOAD_FOLDER = 'app/assets/files'
ALLOWED_EXTENSIONS = {'py'}

# Database connection settings
# DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jotunheimr.db'

# Server settings
PORT = os.environ.get('PORT', 80)
DEBUG = os.environ.get('DEBUG', True)
TESTING = os.environ.get('TESTING', True)
TEMPLATES_AUTO_RELOAD = os.environ.get('TEMPLATES_AUTO_RELOAD', True)
SEND_FILE_MAX_AGE_DEFAULT = os.environ.get('SEND_FILE_MAX_AGE_DEFAULT', 0)
# Load info from the config.yml file
# Path: /config.yml
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_YML_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.yml')
print(f"[*] Loading config from: {CONFIG_YML_PATH}")

"""
config = {}
with open(ROOT_DIR + os.sep + 'config.yml', 'r', encoding='utf-8') as ymlfile:
    try:
        config = yaml.safe_load(ymlfile)
    except yaml.YAMLError as exc:
        print(exc)

TITLE = config.get('title', "Jotunheimr")
SUBTITLE = config.get('subtitle', "Application Dashboard")
LOGO = config.get('logo', "app/assets/tools/solaire.png")
HEADER = config.get('header', True)
USER_CSS_LIST = config.get('stylesheet', ["app/assets/css/user.css"])
for USER_CSS in USER_CSS_LIST:
    if os.path.exists(USER_CSS):
        USER_CSS = os.path.join(os.path.dirname(__file__), USER_CSS)
        print(f"[+] Found user stylesheet: {USER_CSS}")
"""