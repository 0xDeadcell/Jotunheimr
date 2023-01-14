import http.server
import ssl
import subprocess
import os
import argparse
from shutil import which




def get_certbot_certs():
    # Get the hostname of the device
    hostname = subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    print(f"[+] Hostname: {hostname}")
    tld = input("[+] Top-level domain (e.g. website.dev): ").split('//')[-1]
    hostname = hostname + '.' + tld

    # Determine the operating system
    if os.name == 'nt':
        # Windows
        CERTBOT_PATH = which('certbot.exe')
        CERT_PATH = 'C:\\letsencrypt\\live\\' + hostname + '\\'
    else:
        # Linux
        CERTBOT_PATH = which('certbot')
        CERT_PATH = '/etc/letsencrypt/live/' + hostname + '/'

    # Generate a new SSL certificate using certbot
    subprocess.run([CERTBOT_PATH, "certonly", "--standalone", "-d", hostname])


def generate_self_signed_cert(key_file, cert_file):
    print("> openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes")
    # Generate a new self signed SSL certificate
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-keyout', key_file, '-out', cert_file, '-days', '365', '-nodes'])


def start_server(key_file, cert_file):
    # Create the server and specify the handler to handle requests
    server = http.server.HTTPServer(('', 443), http.server.SimpleHTTPRequestHandler)
    #
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    # serve to all addresses
    server.server_address = ('0.0.0.0', 443)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    # Print message how you can connect to the server
    print(f"[+] Connect to the server using https://localhost")
    # Start the server
    server.serve_forever()


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Start a HTTPS server')
    required = parser.add_mutually_exclusive_group(required=True)
    required.add_argument('-g', '--generate_certbot', action='store_true', help='Generate a new SSL CERTBOT certificate')
    required.add_argument('-G', '--generate_self_signed', action='store_true', help='Generate a new self signed SSL certificate')
    required.add_argument('-s', '--start', action='store_true', help='Start the HTTPS server')
    # mandatory arguments for the keyfile and the certfile
    parser.add_argument('-k', '--key_file', type=str, help='The key file', required=False)
    parser.add_argument('-c', '--cert_file', type=str, help='The certificate file', required=False)

    # Parse the arguments
    args = parser.parse_args()
    # validate that the key file and the cert file exist
    if args.start and not (args.key_file and args.cert_file):
        print(f"[!] Please specify the key file (-k) and the certificate file (-c) to generate\n")
        # show the usage
        parser.print_help()
        exit(1) 
    elif not args.key_file and not args.cert_file:
        print(f"[!] Please specify the key file (-k) and the certificate file (-c) to generate\n")
        parser.print_help()
        exit(1)

    args.key_file = os.path.abspath(args.key_file)
    args.cert_file = os.path.abspath(args.cert_file)

    # Generate a new SSL certificate
    if args.generate_certbot:
        get_certbot_certs()
    
    # Generate a self signed SSL certificate
    if args.generate_self_signed:
        generate_self_signed_cert(args.key_file, args.cert_file)

    # Start the HTTPS server
    if args.start:
        # verify that the key file and the cert file exist
        if not os.path.exists(args.key_file) and not os.path.exists(args.cert_file):
            print(f"[!] The key file and the certificate file do not exist")
            exit(1)
        start_server(args.key_file, args.cert_file)