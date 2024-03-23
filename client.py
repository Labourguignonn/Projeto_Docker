from socket import socket, AF_INET, SOCK_DGRAM
import sys
from threading import Thread
import subprocess
import os
import ast

#Passo 1: Criando o socket.
mClientSocket = socket(AF_INET, SOCK_DGRAM)
port = 1234
serverName = 'server'
serverAddress = (serverName, port)

def HandleRequestUdp(mserverSocket):
    message, clientaddress = mClientSocket.recvfrom(8192)
    # DIVIDE A CHAVE DA MENSAGEM
    # msg     = message[4096:8192]
    # Verifica se a chave é valida na CA
    message = 'auth ' + clientaddress
    mClientSocket.sendto(message.encode(), serverAddress)
    chaveCA, clientaddress = mClientSocket.recvfrom(4096)
    ans = chaveCA.decode()
    if (ans == 'Chave publica nao encontrada'):
        # Chave é inválida
        answer = "chave inválida"
    else:    
        # Chave válida
        answer = "chave válida, mensagem recebida"
    mClientSocket.sendto(answer.encode(), serverAddress)
    
if __name__ == "__main__":
    private_key = ''

    if (len(sys.argv) == 2 and sys.argv[1] == 'start'):
        # Comando para obter o nome do contêiner Docker
        bashCommandName = "nslookup $(hostname -i | awk '{print $1}') | awk '/name/ {print $4}' | cut -d'.' -f1"
        # Executando o comando e capturando a saída
        output = subprocess.check_output(['bash', '-c', bashCommandName])
        # Decodificando a saída para UTF-8 e removendo quaisquer espaços em branco extras
        container_name = output.decode('utf-8').strip()
        print(container_name)        
        while True:
            port = int(port)
            container_name = str(container_name)
            mClientSocket.bind(('127.0.0.1', port))
            Thread(target=HandleRequestUdp, args=(mClientSocket,)).start()
    elif len(sys.argv) != 3:
        print("Uso: python3 cliente.py <endereco_cliente> <mensagem>")
        sys.exit(1)
    clientAddress = (sys.argv[1], port)
    key_exists = False
    # Verificar se a chave privada já foi criada
    try:
        with open('private_key.txt', 'r') as f:
            private_key = f.read().strip()
        key_exists = True
    except FileNotFoundError:
        pass
    
    if not key_exists:
        # Se a chave privada não foi encontrada, solicita a criação ao servidor
        message = 'create'
        mClientSocket.sendto(message.encode(), serverAddress)
        private_key_rcv, sAddress = mClientSocket.recvfrom(4096)
        private_key = private_key_rcv.decode()
        # Salvando a chave em um arquivo
        with open('private_key.txt', 'w') as f:
            f.write(private_key)
            print("Chave privada salva com sucesso no arquivo private_key.txt")

    print(f'Chave privada: {private_key}')
    
    # ENVIA MENSAGEM PARA O CLIENTE 
    
    message = sys.argv[1]
    mClientSocket.sendto(message.encode(), clientAddress)
    answer, sAddress = mClientSocket.recvfrom(4096)
    print(answer.decode())