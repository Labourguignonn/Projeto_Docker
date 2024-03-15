from socket import socket, AF_INET, SOCK_DGRAM

# Hands on 4: Key Generator (Asymmetric Key)
# Este script demonstra como gerar uma chave aleatória, criptografar e descriptografar dados usando o algoritmo RSA.

# Caso o seu computador não tenha a biblioteca Crypto
# pip install rsa
import rsa

# Geraçaõ das chaves públicas e privadas
pubkey, privkey = rsa.newkeys(512)

# Dados a serem criptografados
data = b'hello world'

# Criptografa os dados com a chave pública
ciphertext = rsa.encrypt(data, pubkey)
print(f'Ciphertext: {ciphertext.hex()}')

# Descriptografa os dados com a chave privada
plaintext = rsa.decrypt(ciphertext, privkey)

print(f'Plaintext: {plaintext.decode("utf-8")}')


#Passo 1: Criando o socket.
mClientSocket = socket(AF_INET, SOCK_DGRAM)

serverPort = 1234
serverName = 'localhost'

serverAddress = (serverName, serverPort)

for i in range(3):
    # Este loop foi criado apenas para que o cliente conseguisse enviar múltiplas solicitações
    message = input('>>')
    #Enviando a mensagem pelo socket criado.
    mClientSocket.sendto(message.encode(), serverAddress)
    #Recebendo as respostas do servidor.
    data, sAddress = mClientSocket.recvfrom(2048)
    reply = data.decode()
    print(f'Resposta recebida:{reply}')

mClientSocket.close()

serverPort = 1234
serverName = 'localhost'

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))
print('The server is ready to receive')

for i in range(6):
    message, clientAddress = serverSocket.recvfrom(2048)
    req = message.decode()
    print(f'A requisicao foi:{req}')
    rep = 'Hey cliente!'
    serverSocket.sendto(rep.encode(),clientAddress)

serverSocket.close()