import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from socket import socket, AF_INET, SOCK_DGRAM

def generate_key_pair():
    key = RSA.generate(2048)
    return key

def load_public_key(filename):
    with open(filename, 'rb') as f:
        key = RSA.import_key(f.read())
    return key

def save_public_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key.publickey().export_key('PEM'))

# Dicionário para mapear endereços IP às chaves públicas dos clientes
client_public_keys = {}

# Generate server RSA key pair
server_rsa_key_pair = RSA.generate(2048)

# Save server public key
save_public_key(server_rsa_key_pair, 'server_public_key.pem')

# Create socket
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('localhost', 1234))
print("Server online")

try:
    while True:
        # Receive client public key or request
        data, client_address = server_socket.recvfrom(4096)

        # Check if it's a request for public key
        if data.strip().lower().startswith(b'request_public_key'):
            # Extract client ID from the request
            client_id = data.split(b' ')[1].decode()

            # Check if client ID is in the mapping
            if client_id in client_public_keys:
                # Get client public key
                client_public_key = client_public_keys[client_id]

                # Send client public key to client
                server_socket.sendto(client_public_key.publickey().export_key('PEM'), client_address)
            else:
                # If client ID is not found in the mapping, generate a new key pair for the client
                client_rsa_key_pair = generate_key_pair()
                client_public_key = client_rsa_key_pair.publickey().export_key('PEM')
                client_public_keys[client_id] = client_rsa_key_pair

                # Send client public key to client
                server_socket.sendto(client_public_key, client_address)

        else:
            # Otherwise, assume it's a new public key and store it
            client_public_key = RSA.import_key(data)
            client_id = data.split(b' ')[0].decode()  # Extract client ID
            client_public_keys[client_id] = client_public_key

finally:
    server_socket.close()