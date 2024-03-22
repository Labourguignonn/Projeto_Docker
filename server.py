from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from socket import socket, AF_INET, SOCK_DGRAM

def load_private_key(filename):
    with open(filename, 'rb') as f:
        key = RSA.import_key(f.read())
    return key

def save_public_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key.publickey().export_key('PEM'))

def encrypt_rsa(public_key, data):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher_rsa.encrypt(data)
    return encrypted_data

def decrypt_rsa(private_key, encrypted_data):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    return decrypted_data

# Step 1: Create socket
server_socket = socket(AF_INET, SOCK_DGRAM)

# Step 2: Bind socket to address and port
server_socket.bind(('localhost', 1234))

# Receive client private key
client_private_key_data, _ = server_socket.recvfrom(4096)

# Load client private key
client_private_key = load_private_key(client_private_key_data)

# Generate server RSA key pair
server_rsa_key_pair = RSA.generate(2048)

# Save server public key
save_public_key(server_rsa_key_pair, 'server_public_key.pem')

# Encrypt server public key with client public key
server_public_key = server_rsa_key_pair.publickey()
encrypted_server_public_key = encrypt_rsa(client_private_key, server_public_key.export_key('PEM'))

# Send encrypted server public key to client
server_socket.sendto(encrypted_server_public_key, _)

# Handling client request
while True:
    # Receive encrypted AES key
    encrypted_aes_key, _ = server_socket.recvfrom(4096)

    # Receive AES parameters
    nonce = server_socket.recv(16)
    tag = server_socket.recv(16)
    ciphertext = server_socket.recv(4096)

    # Decrypt AES key
    aes_key = decrypt_rsa(client_private_key, encrypted_aes_key)

    # Decrypt data
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    print(f'Decrypted data: {decrypted_data.decode()}')

    # Respond to client
    response = "Data received successfully!"
    server_socket.sendto(response.encode(), _)
