from flask import Flask, request, render_template, jsonify, url_for, redirect, send_from_directory, send_file
from app import app, load_config
from werkzeug.utils import secure_filename
from PIL import Image
import subprocess
import mimetypes
from zipfile import ZipFile
import json
import os
import re


# Set the path to the directory containing this file
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
print(f"[+] Root path: {ROOT_PATH}")

# Set the allowed extensions for files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DEFAULT_LOGO = 'assets/tools/asterisk.png'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    refresh_config()
    # Get the list of apps
    title = app.config.get('title', "Jotunheimr")
    subtitle = app.config.get('subtitle', "Application Dashboard")
    logo = app.config.get('logo', "/static/img/logo.png")
    favicon = app.config.get('favicon', '/static/favicon.ico')
    header = app.config.get('header', True)
    footer = app.config.get('footer', "")
    user_css = app.config.get('stylesheet', "app/assets/css/user.css")
    #print(f"[+] User CSS: {user_css}")
    apps = []
    app_data = {}
    app_tags = []
    for app_name in os.listdir(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps'))):
        app_data = get_app_details(app_name)
        apps.append(app_data)
        if (app_data.get('tag', None) is not None) and (app_data.get('tag', None) not in app_tags):
            app_tags.append(app_data['tag'])
    return render_template('index.html', apps=apps, app_tags=app_tags, favicon=favicon, footer=footer, title=title, subtitle=subtitle, logo=logo, header=header, user_css=user_css, app_data=app_data)


@app.route('/app/<app_name>')
def render_app(app_name):
    refresh_config()
    # note that we set the 404 status explicitly
    title = app.config.get('title', "Jotunheimr")
    subtitle = app_name.title()
    logo = app.config.get('logo', "/static/img/logo.png")
    header = app.config.get('header', True)
    user_css = app.config.get('stylesheet', "app/assets/css/user.css")

    # Check that the app exists
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))):
        return render_template('404.html')
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'details.json'))):
        return render_template('404.html')
    app_data = get_app_details(app_name)

    # if the app has a custom url, and it's enabled, redirect to that
    if (app_data.get('custom_url', '') is not None) and (app_data.get('enable_custom_url', False) is not False):
        print(f"[!] Redirecting to custom url: {app_data['custom_url']}")
        # if the custom url is the same as the app name, render the app
        print('"' + app_data.get('custom_url') + '"')
        if app_data['custom_url'] == app_name or app_data.get('custom_url').strip() == '':
            return render_template('user_app_template.html', app_data=app_data, title=title, subtitle=subtitle, logo=logo, header=header, user_css=user_css)

        else:
            # open the custom url in a new tab
            return redirect(app_data['custom_url'], code=302)
    else:
        if app_data is None:
            return render_template('404.html')
        else:
            return render_template('user_app_template.html', app_data=app_data, title=title, subtitle=subtitle, logo=logo, header=header, user_css=user_css)


@app.route('/', methods=['POST'])
def add_app():
    # replace any non-alphanumeric characters with nothing, keep spaces
    app_name = re.sub(r'[^a-zA-Z0-9 ]', '', request.form.get('app_name', '')).lower()
    app_desc = request.form.get('app_desc', '')
    app_tag = request.form.get('app_tag', 'Misc').title()
    app_custom_url = request.form.get('app_custom_url', '')
    app_enable_custom_url = request.form.get('app_enable_custom_url', False)
    if app_tag.strip() == '':
        app_tag = 'Misc'
    app_image = request.files['app_image']
    default_image = None
    if app_name == '':
        if app.debug:
            print(f"Failed to create app: No valid app name provided")
        return redirect(url_for('index'))
    
    # using the default image
    if not app_image:                                                                                                                                               
        if app.debug:
            print("[!] No image provided, using default image")
        # check to see if the image is in assets/tools/<app_name> first, if so use that
        # otherwise use the default image at assets/tools/asterisk.png
        # find a valid image for png, jpg, jpeg, and gif
        filename_path = os.path.normpath(os.path.join(ROOT_PATH, f'assets/tools/', app_name))
        valid_image_logo = [filename_path + '.' + ext for ext in ALLOWED_EXTENSIONS if os.path.exists(filename_path + '.' + ext)]
        if len(valid_image_logo) > 0:
            print(f"Found image for {app_name}!")
            default_image = f'assets/tools/{app_name}.{valid_image_logo[0].split(".")[-1]}'
        else:
            print("Using default image")
            default_image = DEFAULT_LOGO
    # check to see if the filetype is valid
    elif not allowed_file(app_image.filename):
        print(f"Failed to create app {app_name}: Invalid file type ({app_image.filename}), must be: {ALLOWED_EXTENSIONS}")
        return redirect(url_for('index'))
    app_name = app_name.replace(' ', '_')
    
    app_folder = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))
    if os.path.exists(app_folder):
        print(f"Failed to create app {app_name}: App already exists")
        return redirect(url_for('index'))
    # create the app folder
    os.makedirs(app_folder, exist_ok=True)
    # create the user_scripts folder
    os.makedirs(os.path.normpath(os.path.join(app_folder, 'user_scripts')), exist_ok=True)
    # create the script_log.txt file
    with open(os.path.normpath(os.path.join(app_folder, 'user_scripts', 'script_log.txt')), 'w') as f:
        f.write('')
    # create a default script
    with open(os.path.normpath(os.path.join(app_folder, 'user_scripts', 'script.py')), 'w') as f:
        f.write("print('Hello World!')")
    
    if not default_image:
        # save the image depending on the file type
        app_image.save(os.path.normpath(os.path.join(app_folder, 'user_logo' + os.path.splitext(app_image.filename)[1])))
    else:
        # default images *should* be .png
        app_image.filename = 'user_logo.png'
        # Copy the default image to the app folder
        with open(os.path.normpath(os.path.join(app_folder, 'user_logo.png')), 'wb') as f:
            with open(os.path.normpath(os.path.join(ROOT_PATH, default_image)), 'rb') as f2:
                f.write(f2.read())
    
    # Save the details of the app to a json file
    with open(os.path.normpath(os.path.join(app_folder, 'details.json')), 'w') as f:
        f.write(json.dumps({
            'name': app_name,
            'image': os.path.join(app_folder, 'user_logo' + os.path.splitext(app_image.filename)[1]),
            'desc': app_desc,
            'tag': app_tag,
            'custom_url': app_custom_url if app_enable_custom_url else "",
            'enable_custom_url': app_enable_custom_url,
    }))
    if app.debug:
        print(f"Created app {app_name}:\nFolder: {app_folder}\nImage: {app_image.filename}\nDescription: {app_desc}\nTag: {app_tag}\nCustom URL: {app_custom_url}\nEnable Custom URL: {app_enable_custom_url}")
    
    return redirect(url_for('index'))

# Refresh the config file
@app.route('/api/refresh', methods=['GET'])
def refresh_config():
    old_config = app.config
    app.config.from_pyfile('config.py')
    config_yml_path = app.config.get('CONFIG_YML_PATH', ROOT_PATH + os.sep + 'config.yml')
    if os.path.exists(config_yml_path):
        try:
            new_config = load_config(config_yml_path)
            app.config.update(new_config)
        except Exception as e:
            print(f"Failed to load config from {config_yml_path}: {e}")
    if app.debug:
        print(f"[+] Config refreshed from `{config_yml_path}`")
        # Check if the values have changed
        for key in app.config:
            try:
                if old_config[key] != app.config[key]:
                    print(f"[+] Config value changed: {key}: {old_config[key]} -> {app.config[key]}")
            except KeyError:
                print(f"[*] Config value removed: {key}: {old_config[key]}")
    return app.config


@app.route('/api/app/<app_name>/update', methods=['POST'])
def update_app_details(app_name):
    # update the details of an app with provided data from a form
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))):
        return render_template('404.html')
    with open(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'details.json')), 'r') as f:
        app_data = json.loads(f.read())
    if request.files.get('image', None) is not None:
        app_image = request.files.get('image', None)
        if app_image.filename.strip() != '':
            # Null filenames may contain whitespace
            print(f"Updating image for {app_name} to: `{app_image.filename}`")
            if not allowed_file(app_image.filename):
                return f"Invalid file type {app_image.filename}, must be: {', '.join(ALLOWED_EXTENSIONS)}"
            # scale the image to 512x512 if it is not a gif
            if os.path.splitext(app_image.filename)[1] != '.gif':
                app_image = Image.open(app_image)
                app_image = app_image.resize((512, 512), Image.ANTIALIAS)
            # save the image depending on the file type
            app_image.save(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'user_logo' + os.path.splitext(app_image.filename)[1])))
    
    if request.form.get('tag', None) is not None:
        app_tag = request.form.get('tag', None)
        app_data['tag'] = app_tag.title()
    if request.form.get('desc', None) is not None:
        app_desc = request.form.get('desc', None)
        app_data['desc'] = app_desc
    if request.form.get('name', None) is not None:
        print(app_data)
        old_app_folder = os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))
        app_name = request.form.get('name', '').replace(' ', '_').lower()
        app_data['name'] = app_name
        print(app_data['name'])
        new_app_folder = os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name))
        print(f"Renaming app folder from `{old_app_folder}` to `{new_app_folder}`")
        os.rename(old_app_folder, new_app_folder)
    if request.form.get('custom_url', None) is not None:
        app_custom_url = request.form.get('custom_url', None)
        app_data['custom_url'] = app_custom_url
    if request.form.get('enable_custom_url', False):
        app_enable_custom_url = request.form.get('enable_custom_url')
        app_data['enable_custom_url'] = app_enable_custom_url
    if app_data['custom_url'] == "":
        app_data['enable_custom_url'] = "off"
    print("[+] Updated app" + app_name + ":\n" + '\n'.join([f'{k}: {v}' for k, v in app_data.items()]))
    with open(os.path.normpath(os.path.join(ROOT_PATH, f'assets/apps', app_name, 'details.json')), 'w') as f:
        f.write(json.dumps(app_data))
    return redirect(url_for('index'))

        
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


# redirect to the correct image based on the name of the app
@app.route('/api/app/<app_name>/image', methods=['GET'])
def get_app_image(app_name):
    if request.path.startswith('/api/app/') and request.path.endswith('/image'):
        # Get the full path of the image
        try:
            image = [image for image in os.listdir(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))) if image.startswith('user_logo') and allowed_file(image)][0]
        except IndexError:
            # no user logo found, return the default logo
            image = os.path.normpath(os.path.join(ROOT_PATH, DEFAULT_LOGO))
        # serve it from the url /api/app/<app_name>/image/<image_name>
        url = url_for('get_app_image_filetype', app_name=app_name, file_name=image)
        # render the url
        return redirect(url)
    return f"Invalid request", 400


@app.route('/api/app/<app_name>/image/<file_name>', methods=['GET'])
def get_app_image_filetype(app_name, file_name):
    # redirect to the correct image based on the file type
    if not os.path.exists(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, file_name))):
        return f"File {file_name} not found", 404
    # return the correct image based on the file type
    # check the directory for user_logo, and return the first one found
    try:
        image = [image for image in os.listdir(os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))) if image.startswith('user_logo') and allowed_file(image)][0]
    except IndexError:
        # if no user_logo is found, return a default image
        image = os.path.normpath(os.path.join(ROOT_PATH, DEFAULT_LOGO))
    # make sure to return the correct mimetype, with the correct extension
    image_path = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name))
    image_name = image.split('/')[-1]
    # set the content length to the size of the file
    return send_from_directory(image_path, image_name, as_attachment=True)


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


@app.route('/api/app/<app_name>/run_script', methods=['POST', 'GET'])
def run_script(app_name):
    args = request.args.get('args', '')
    if request.method == 'POST':
        args = request.form.get('script_arguments', '')
    print(f"Running script for {app_name} with args: {args}")
    script_path = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'script.py'))
    if os.path.exists(script_path):
        # Popen the script with stdout and stderr redirected
        try:
            out, err = subprocess.Popen(['python3', script_path, *args.split()], cwd=os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts'), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        except Exception as e:
            print("Invalid File or Python Version" + err + e)
        try:
            out, err = subprocess.Popen(['py', script_path, *args.split()], cwd=os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts'), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        out = b''
        err = b''
        print(f"{app_name} doesn't have a script")
    if app.debug:
        print(f"Ran script for {app_name} at {script_path}:\nSTDOUT:\n{out.decode('utf-8')}\nSTDERR:\n{err.decode('utf-8')}")
    app_details = get_app_details(app_name)
    if app_details['custom_url']:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('render_app', app_name=app_name))

@app.route('/api/app/<app_name>/get_script_log', methods=['GET'])
def get_script_log(app_name):
    script_log_path = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'script_log.txt'))
    if os.path.exists(script_log_path):
        with open(script_log_path, 'r') as f:
            return f.read().replace('\n', '<br>')
    else:
        return "No script log found"

@app.route('/api/app/<app_name>/download_script_output', methods=['GET'])
def download_script_output(app_name):
    script_output_path = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts'))
    output_files = [f for f in os.listdir(script_output_path) if os.path.isfile(os.path.join(script_output_path, f)) and f != 'script.py' and f != 'script_log.txt']
    # zip the found files
    if len(output_files) > 0:
        zip_path = os.path.normpath(os.path.join(ROOT_PATH, 'assets/apps', app_name, 'user_scripts', 'output.zip'))
        with ZipFile(zip_path, 'w') as zip:
            for file in output_files:
                zip.write(os.path.join(script_output_path, file), file)
        return send_file(zip_path, as_attachment=True)
    else:
        return "No output files found"

# default route for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    logo = app.config.get('logo', "app/assets/tools/logo.png")
    if app.debug:
        print(f"Page not found: {request.url}")
    return render_template('404.html')



# upgrade http to https
# @app.before_request
# def before_request():
#     if not request.is_secure and app.config.get("redirect_to_https", False):
#         print("[!] Redirecting request to HTTPS")
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)



app.jinja_env.globals.update(get_script_log=get_script_log)