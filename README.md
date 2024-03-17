Para rodar as aplicações disponíveis nesse repositório, siga os passos a seguir (linux):


```
git clone rep
```

Abra o terminal e entre na pasta que deseja rodar a aplicação, recomenda-se utilizar o Python3:

```
Python3 code.py
```

Lembre-se que, para aplicações cliente-servidor, será necessário utilizar dois terminais, um para o cliente e outro para o servidor.

COMANDOS USADOS:


Rodar os contêineres: 
```
docker-compose app -d
```

Remove todos os contêineres: 
```
docker rm -f $(docker ps -aq)
```

Construir a imagem do contêiner do cliente: 
```
docker build -t cliente:latest -f Dockerfile.client .
```

Construir a imagem do contêiner do servidor: 
```
docker build -t server:latest -f Dockerfile.server .
```

Remover recursos não utilizados pelo docker: 
```
docker system prune
```

Lista de todas as redes do docker: 
```
docker network ls
```
