from app import app

if __name__ == '__main__':
    cert_path, key_path = app.search_certificates()
    if cert_path and key_path:
        # Start the app with HTTPS support
        app.run(ssl_context=(cert_path, key_path), port=80)
    else:
        # Start the app with HTTP
        print("Certificates not found, running on HTTP.")
        app.run(port=80)