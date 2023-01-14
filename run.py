import os
from app import app, setup_https

if __name__ == '__main__':
    cert_path, key_path = app.search_certificates()
    # check if https is enabled in the config
    https_enabled = app.config['https']
    if https_enabled:
        print("[+] HTTPS enabled in config.yml")
        if cert_path and key_path:
            print("[+] Certificates found, running on HTTPS.")
            # Start the app with HTTPS support
            # proxy the port 80 to 443 (windows)
            app.run(host='0.0.0.0', ssl_context=(cert_path, key_path), port=443)
        else:
            os.makedirs('app/certs', exist_ok=True)
            # Generate self-signed certificates
            print("[!] Certificates not found, generating self-signed certificates.")
            setup_https.generate_self_signed_cert(key_file='app/certs/key.pem', cert_file='app/certs/cert.pem')
            # Start the app with HTTPS support
            print("[+] Certificates generated, running on HTTPS.")
            app.run(host='0.0.0.0', ssl_context=('app/certs/cert.pem', 'app/certs/key.pem'), port=443)
    else:
        # Start the app with HTTP
        print("[!] Certificates not found, running on HTTP.")
        app.run(host='0.0.0.0', port=80)