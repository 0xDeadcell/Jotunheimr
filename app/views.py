from flask import Flask, request, render_template, jsonify, url_for, redirect, send_from_directory
from app import app
from werkzeug.utils import secure_filename
import subprocess
import json
import os
import re


# Set the path to the directory containing this file
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Set the allowed extensions for files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # Get the list of apps
    title = app.config.get('TITLE', "Jotunheimr")
    subtitle = app.config.get('SUBTITLE', "Application Dashboard")
    logo = app.config.get('LOGO', "app/assets/tools/solaire.png")
    header = app.config.get('HEADER', True)
    user_css = app.config.get('USER_CSS', "app/assets/css/user.css")
    apps = []
    app_tags = []
    for app_name in os.listdir(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps'))):
        app_data = get_app_details(app_name)
        apps.append(app_data)
        if (app_data.get('tag', None) is not None) and (app_data.get('tag', None) not in app_tags):
            app_tags.append(app_data['tag'])
    return render_template('index.html', apps=apps, app_tags=app_tags, title=title, subtitle=subtitle, logo=logo, header=header, user_css=user_css)

# default route for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    if app.debug:
        print(f"Page not found: {request.url}")
    return render_template('404.html')


@app.route('/app/<app_name>')
def render_app(app_name):
    # Check that the app exists
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))):
        return render_template('404.html')
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'details.json'))):
        return render_template('404.html')
    app_data = get_app_details(app_name)
    return render_template('user_app_template.html', app_data=app_data)


@app.route('/', methods=['POST'])
def add_app():
    app_name = re.sub(r'\W+', '', request.form['app_name']).lower()
    app_desc = request.form['app_desc']
    app_tag = request.form['app_tag'].title()
    app_image = request.files['app_image']
    default_image = None
    if app_name == '':
        if app.debug:
            print(f"Failed to create app: No valid app name provided")
        return redirect(url_for('index'))
    if not app_image:
        if app.debug:
            print("No image provided")
        # check to see if the image is in assets/tools/<app_name> first, if so use that
        # otherwise use the default image at assets/tools/asterisk.png
        if os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, f'assets/tools/{app_name}.png'))):
            print(f"Found image for {app_name}!")
            default_image = f'assets/tools/{app_name}.png'
        else:
            print("Using default image")
            default_image = 'assets/tools/asterisk.png'
    elif not allowed_file(app_image.filename):
        print(f"Failed to create app {app_name}: Invalid file type, must be .png, .jpg, .jpeg or .gif")
        return redirect(url_for('index'))
    
    app_folder = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))
    if os.path.exists(app_folder):
        print(f"Failed to create app {app_name}: App already exists")
        return redirect(url_for('index'))
    os.makedirs(app_folder, exist_ok=True)
    if not default_image:
        app_image.save(os.path.normpath(os.path.join(app_folder, 'user_logo.png')))
    else:
        os.symlink(os.path.normpath(os.path.join(ROOT_PATH, default_image)), os.path.normpath(os.path.join(app_folder, 'user_logo.png')))
    # Save the details of the app to a json file
    with open(os.path.normpath(os.path.join(app_folder, 'details.json')), 'w') as f:
        f.write(json.dumps({
            'name': app_name,
            'image': os.path.join(app_folder, 'user_logo.png'),
            'desc': app_desc,
            'tag': app_tag,
    }))
    if app.debug:
        print(f"Created app {app_name}:\nFolder: {app_folder}\nImage: {app_image.filename}\nDescription: {app_desc}\nTag: {app_tag}")
    
    print(app_name)
    return redirect(url_for('render_app', app_name=app_name))


@app.route('/api/app/<app_name>/update', methods=['POST', 'GET'])
def update_app_details(app_name):
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))):
        return render_template('404.html')
    with open(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'details.json')), 'r') as f:
        app_data = json.loads(f.read())
    if request.args.get('tag', None) is not None:
        app_tag = request.args.get('tag', None)
        app_data['tag'] = app_tag
    if request.args.get('description', None) is not None:
        app_desc = request.args.get('description', None)
        app_data['desc'] = app_desc
    if request.args.get('name', None) is not None:
        old_app_folder = os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))
        app_name = request.args.get('name', None)
        app_data['name'] = app_name
        new_app_folder = os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))
        os.rename(old_app_folder, new_app_folder)
    with open(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'details.json')), 'w') as f:
        f.write(json.dumps(app_data))
    return redirect(url_for('render_app', app_name=app_name))

        
@app.route('/api/app/<app_name>/delete', methods=['POST'])
def delete_app(app_name):
    app_folder = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))
    if os.path.exists(app_folder):
        # walk the directory and delete all files
        for root, dirs, files in os.walk(app_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(app_folder)
        if app.debug:
            print(f"Deleted app {app_name}:\nFolder: {app_folder}")
    return redirect(url_for('index'))


@app.route('/api/get_apps', methods=['GET'])
def get_apps():
    apps = []
    for app in os.listdir(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps'))):
        if os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app, 'details.json'))):
            with open(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app, 'details.json')), 'r') as f:
                apps.append(json.loads(f.read()))
    return jsonify(apps)


@app.route('/api/app/<app_name>/image', methods=['GET'])
def get_app_image(app_name):
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))):
        return render_template('404.html')
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_logo.png'))):
        return render_template('404.html')
    download_flag = request.args.get('download', False)
    return send_from_directory(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name)), 'user_logo.png', as_attachment=download_flag)


@app.route('/api/app/<app_name>/details', methods=['GET'])
def get_app_details(app_name):
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))):
        return render_template('404.html')
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'details.json'))):
        return render_template('404.html')
    assert os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'details.json')))
    if os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'details.json'))):
        download_flag = request.args.get('download', False)
        if download_flag:
            return send_from_directory(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name)), 'details.json', as_attachment=download_flag)
        with open(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'details.json')), 'r') as f:
            try:
                return json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return "Error: Invalid JSON file"
    return render_template('404.html')


@app.route('/api/app/<app_name>/upload_script', methods=['POST'])
def upload_script(app_name):
    script = request.files['script']
    if not script.filename.endswith('.py'):
        print(f"[!] Failed to upload script for {app_name}: Invalid file type, must be .py")
        # return a popup saying that the file type is invalid
        return redirect(url_for('render_app', app_name=app_name))
    os.makedirs(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts')), exist_ok=True)
    try:
        try:
            os.remove(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'script.py')))
        except Exception as e:
            if app.debug:
                print(f"Failed to remove old script for {app_name}: {e}")
        script.save(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'script.py')))
    except Exception as e:
        if app.debug:
            print(f"Failed to upload script for {app_name}: {e}")
    if app.debug:
        print(f"Successfuly uploaded script for {app_name}: {script.filename}")
    return redirect(url_for('render_app', app_name=app_name))


@app.route('/api/app/<app_name>/run_script', methods=['POST'])
def run_script(app_name):
    print(f"Running script for {app_name}...")
    script_path = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'script.py'))
    if os.path.exists(script_path):
        # Popen the script with stdout and stderr redirected
        try:
            out, err = subprocess.Popen(['python3', script_path], cwd=os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts'), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        except Exception as e:
            print("Invalid File or Python Version" + err + e)
        try:
            out, err = subprocess.Popen(['py', script_path], cwd=os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts'), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        except Exception as e:
            print(e)
        # Save the output to a file
        with open(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'script_log.txt')), 'w') as f:
            f.write("STDOUT:\n")
            f.write(out.decode('utf-8'))
            f.write("\nSTDERR:\n")
            f.write(err.decode('utf-8'))
        # return jsonify({'out': out.decode('utf-8'), 'err': err.decode('utf-8')}) to the user
        
    else:
        # Handle the error if the script doesn't exist
        print(f"{app_name} doesn't have a script")
    if app.debug:
        print(f"Ran script for {app_name} at {script_path}:\nSTDOUT:\n{out.decode('utf-8')}\nSTDERR:\n{err.decode('utf-8')}")

    return redirect(url_for('render_app', app_name=app_name))
