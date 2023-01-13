from flask import Flask
import yaml
import os


# search for cert.pem and key.pem files in the current directory and subdirectories
def search_certificates():
    cert_path = None
    key_path = None
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "cert.pem":
                cert_path = os.path.join(root, file)
            if file == "key.pem":
                key_path = os.path.join(root, file)
    return cert_path, key_path

# get operating system
def get_os():
    if os.name == 'nt':
        return 'windows'
    else:
        return 'linux'


# load config.yml file
def load_config(config_path):
    config = {}
    with open(config_path, 'r', encoding='utf-8') as ymlfile:
        try:
            config = yaml.safe_load(ymlfile)
        except yaml.YAMLError as exc:
            print(exc)
    return config

# Create the application instance
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.search_certificates = search_certificates

# Import the views
from app import views