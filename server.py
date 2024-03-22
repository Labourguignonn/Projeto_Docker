from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Dicionário para mapear endereços IP às chaves públicas dos clientes
client_public_keys = {}

serverPort = 1234
serverName = 'server'

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))
print('The server is online')

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

def HandleRequestUdp(mserverSocket):
    # message, clientaddress = serverSocket.recvfrom(2048)
    message, clientaddress = serverSocket.recvfrom(4096)
    req = message.decode()
    print(f'Requisicao recebida de {clientaddress}')
    print(f'A requisicao foi:{req}')
    if req =='create':
        # CRIA A CHAVE, ADICIONA NO DICIONARIO VINCULANDO COM O IP E RETORNA A CHAVE PRIVADA PARA O CLIENTE
        key = generate_key_pair()
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        rep = private_key
        # SALVA A CHAVE NO DICIONARIO
        client_public_keys[clientaddress[0]] = private_key 
    else:    
        # FAZ AUTENTICACAO DA CHAVE PUBLICA PASSADA CONSULTANDO O DICIONARIO
        # ...
        rep = b'teste'
    mserverSocket.sendto(rep, clientaddress)

while True:
    Thread(target=HandleRequestUdp, args=(serverSocket,)).start()