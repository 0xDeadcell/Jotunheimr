from flask import Flask
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


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.search_certificates = search_certificates
app.config_yml = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep + 'config.yml')
# Import the views
from app import views