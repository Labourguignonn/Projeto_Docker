from socket import socket, AF_INET, SOCK_DGRAM
import sys

#Passo 1: Criando o socket.
mClientSocket = socket(AF_INET, SOCK_DGRAM)
port = 1234
serverName = 'server'

serverAddress = (serverName, port)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Uso: python3 cliente.py <endereco_cliente>")
        sys.exit(1)
    clientAddress = (sys.argv[1], port)
    
    message = 'create'
    #Enviando a mensagem pelo socket criado.
    mClientSocket.sendto(message.encode(), serverAddress)
    #Recebendo as respostas do servidor.
    data, sAddress = mClientSocket.recvfrom(2048)
    reply = data.decode()
    print(f'Resposta recebida:{reply}')

    mClientSocket.close()