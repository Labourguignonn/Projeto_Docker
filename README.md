Para rodar as aplicações disponíveis nesse repositório, siga os passos a seguir (linux):


```
git clone rep
```
Lembre-se que, para aplicações cliente-servidor, será necessário utilizar dois terminais, um para o cliente e outro para o servidor.

COMANDOS USADOS:

Remove todos os contêineres: 
```
docker rm -f $(docker ps -aq)
```

Remover todas redes do docker: 
```
docker network prune
```

Rodar os contêineres: 
```
docker-compose up -d
```

Construir a imagem do contêiner do cliente: 
```
docker build -t cliente:latest -f Dockerfile.client .
```

Construir a imagem do contêiner do servidor: 
```
docker build -t server:latest -f Dockerfile.server .
```

Lista de todas as redes do docker: 
```
docker network ls
```
Abrir o terminal do containers: 
```
 docker rm -f $(docker ps -aq)
```
Abrir o container específico para rodar: 
```
docker exec -it cliente1 /bin/bash
```

```
docker exec -it cliente0 python3 /app/client.py cliente1
```