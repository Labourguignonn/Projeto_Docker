import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from socket import socket, AF_INET, SOCK_DGRAM

# while(1): 
#  i = 0
# Função para gerar o par de chaves RSA

# Define flag do client0
flags = 0

def generate_rsa_key_pair():
    key = RSA.generate(2048)
    return key

# Função para salvar a chave privada em um arquivo
def save_private_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key.export_key('PEM'))

# Função para salvar a chave pública em um arquivo
def save_public_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key.publickey().export_key('PEM'))

# Função para carregar a chave privada de um arquivo
def load_private_key(filename):
    with open(filename, 'rb') as f:
        key = RSA.import_key(f.read())
    return key

# Função para criptografar usando RSA
def encrypt_rsa(public_key, data):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher_rsa.encrypt(data)
    return encrypted_data

# Função para descriptografar usando RSA
def decrypt_rsa(private_key, encrypted_data):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    return decrypted_data

# Função para criar um hash da mensagem usando SHA-256
def hash_message(message):
    return hashlib.sha256(message.encode()).digest()

# Função para enviar mensagem criptografada
def send_encrypted_message(socket, message, public_key):
    encrypted_message = encrypt_rsa(public_key, message)
    socket.send(encrypted_message)

# Função para receber mensagem criptografada
def receive_encrypted_message(socket, private_key):
    encrypted_message = socket.recv(4096)
    decrypted_message = decrypt_rsa(private_key, encrypted_message)
    return decrypted_message.decode()

if __name__ == "__main__":
    # Verifica se o número correto de argumentos foi fornecido
    if len(sys.argv) != 2:
        print("Uso: python3 cliente.py <endereco_servidor>")
        sys.exit(1)

    # Obtém o endereço do cliente a partir dos argumentos de linha de comando
    client_address = sys.argv[1]

    # Define o nome do server e as portas do server e client
    server_address = ("server", 1234)
    # server_port = 1234
    client_port = 1234

    # Step 1: Create two sockets one for the server, another for the client
    server_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket = socket(AF_INET, SOCK_DGRAM)

    # Step 2: Transform socket into a client socket
    #server_socket.connect(("server", server_port))
    #client_socket.connect((client_address, client_port))

    # Generate RSA key pair
    rsa_key_pair = generate_rsa_key_pair()

    # Save private key
    save_private_key(rsa_key_pair, 'client_private_key.pem')

    # Encrypt and send private key to server
    with open('client_private_key.pem', 'rb') as f:
        private_key_data = f.read()

    print(len(private_key_data))

    server_socket.sendto(private_key_data,server_address,flags)

    # Receive encrypted public key from the server
    server_public_key_data = server_socket.recv(4096)

    # Load server public key
    server_public_key = RSA.import_key(server_public_key_data)

    # Data to be encrypted
    #data = input("Digite o texto a ser criptografado: ").encode('utf-8')

    # Generate a random AES key
    #aes_key = get_random_bytes(16)

    # Encrypt data using AES
    #cipher = AES.new(aes_key, AES.MODE_EAX)
    #ciphertext, tag = cipher.encrypt_and_digest(data)

    # Encrypt AES key using RSA public key
    #encrypted_aes_key = encrypt_rsa(server_public_key, aes_key)

    # Send encrypted AES key and AES encrypted data to the server
    # server_socket.sendto(encrypted_aes_key,server_address,flags)
    # server_socket.sendto(cipher.nonce,server_address,flags)
    # server_socket.sendto(tag,server_address,flags)
    # server_socket.sendto(ciphertext,server_address,flags)

    # Receive and decrypt response from server
    # response = server_socket.recv(4096)
    # decrypted_response = decrypt_rsa(rsa_key_pair, response)
    # print(f'Response from server: {decrypted_response}')

    # Close socket
    server_socket.close()