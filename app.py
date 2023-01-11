from flask import Flask, request, render_template, jsonify, url_for, redirect
from flask_scss import Scss
from werkzeug.utils import secure_filename
import subprocess
import dotenv
import json
import os


# Set the path to the directory containing this file
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Create the Flask app
app = Flask(__name__)
app.debug = True
app.config.from_pyfile('config.py')

# Set the allowed extensions for files
ALLOWED_EXTENSIONS = {'py', 'png', 'jpg', 'jpeg', 'gif'}



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

# default route for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')


@app.route('/', methods=['POST'])
def add_app():
    app_name = request.form['app_name']
    app_desc = request.form['app_desc']
    app_tag = request.form['app_tag']
    app_image = request.files['app_image']
    print(app_name, app_desc, app_tag, app_image)
    
    # Check if the image file is valid
    if not allowed_file(app_image.filename):
        return redirect(url_for('index'))
    # Save the file to the server
    filename = secure_filename(app_image.filename)
    app_folder = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))
    print(app_folder)
    os.makedirs(app_folder, exist_ok=True)
    app_image.save(os.path.normpath(os.path.join(app_folder, 'user_logo.png')))

    # Save the details of the app to a json file
    with open(os.path.normpath(os.path.join(app_folder, 'details.json')), 'w') as f:
        f.write(json.dumps({
            'name': app_name,
            'image': os.path.join(app_folder, 'user_logo.png'),
            'desc': app_desc,
            'tag': app_tag,
    }))
    return redirect(url_for('app', app_name=app_name))

@app.route('/app/<app_name>')
def render_app(app_name):
    with open(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'details.json')) as f:
        app_data = json.load(f)
    return render_template('user_app_template.html', app_data=app_data)


@app.route('/app/<app_name>/upload_script', methods=['POST'])
def upload_script(app_name):
    script = request.files['script']
    # Check if the script file is valid
    if not allowed_file(script.filename):
        return redirect(url_for('app', app_name=app_name))
    # Save the file to the server
    filename = secure_filename(script.filename)
    script.save(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', filename))
    return redirect(url_for('app', app_name=app_name))


@app.route('/app/<app_name>/run_script')
def run_script(app_name):
    script_path = os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'script.py')
    if os.path.exists(script_path):
        os.system(f'python {script_path}')
    else:
        # Handle the error if the script doesn't exist
        pass
    return redirect(url_for('app', app_name=app_name))


if __name__ == '__main__':
    app.run(port=80)
