from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from socket import socket, AF_INET, SOCK_DGRAM


#precisa informar pra qual servidor e qual o cliente

def generate_rsa_key_pair():
    key = RSA.generate(2048)
    return key

def save_private_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key.export_key('PEM'))

def save_public_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key.publickey().export_key('PEM'))

def load_private_key(filename):
    with open(filename, 'rb') as f:
        key = RSA.import_key(f.read())
    return key

def encrypt_rsa(public_key, data):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher_rsa.encrypt(data)
    return encrypted_data

def decrypt_rsa(private_key, encrypted_data):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    return decrypted_data

def hash_message(message):
    return hashlib.sha256(message.encode()).digest()

def send_encrypted_message(socket, message, public_key):
    encrypted_message = encrypt_rsa(public_key, message)
    socket.send(encrypted_message)

def receive_encrypted_message(socket, private_key):
    encrypted_message = socket.recv(4096)
    decrypted_message = decrypt_rsa(private_key, encrypted_message)
    return decrypted_message.decode()

# Step 1: Create socket
client_socket = socket(AF_INET, SOCK_DGRAM)

# Step 2: Transform socket into a client socket
client_socket.connect(('localhost', 1234))

# Generate RSA key pair
rsa_key_pair = generate_rsa_key_pair()

# Save private key
save_private_key(rsa_key_pair, 'client_private_key.pem')

# Encrypt and send private key to server
with open('client_private_key.pem', 'rb') as f:
    private_key_data = f.read()

client_socket.send(private_key_data)

# Receive encrypted public key from the server
server_public_key_data = client_socket.recv(4096)

# Load server public key
server_public_key = RSA.import_key(server_public_key_data)

# Data to be encrypted
data = input("Digite o texto a ser criptografado: ").encode('utf-8')

# Generate a random AES key
aes_key = get_random_bytes(16)

# Encrypt data using AES
cipher = AES.new(aes_key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

# Encrypt AES key using RSA public key
encrypted_aes_key = encrypt_rsa(server_public_key, aes_key)

# Send encrypted AES key and AES encrypted data to the server
client_socket.send(encrypted_aes_key)
client_socket.send(cipher.nonce)
client_socket.send(tag)
client_socket.send(ciphertext)

# Receive and decrypt response from server
response = client_socket.recv(4096)
decrypted_response = decrypt_rsa(rsa_key_pair, response)
print(f'Response from server: {decrypted_response}')

# Close socket
client_socket.close()
