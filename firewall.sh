#!/bin/bash

# Limpar todas as regras existentes
iptables -F

# Adquirir o endereço IP do host local
LOCAL_IP=$(hostname -I | awk '{print $1}')
MAQUINA_ATUAL=$(hostname)
IPServer=$(nslookup server)
IPCliente0=$(nslookup cliente0)
IPCliente1=$(nslookup cliente1)
IPCliente2=$(nslookup cliente2)
IPCliente3=$(nslookup cliente3)
IPCliente4=$(nslookup cliente4)
IPCliente5=$(nslookup cliente5)

# iptables -A INPUT -j DROP
iptables -A FORWARD -j DROP
iptables -A OUTPUT -j DROP

if [ "$MAQUINA_ATUAL" = "server" ]; then
    iptables -A INPUT -j DROP
elif [ "$MAQUINA_ATUAL" = "cliente0" ]; then
    iptables -A OUTPUT -d "$IPCliente1" -j ACCEPT
    iptables -A OUTPUT -d "$IPCliente5" -j ACCEPT
elif [ "$MAQUINA_ATUAL" = "cliente1" ]; then
    iptables -A OUTPUT -d "$IPCliente0" -j ACCEPT
    iptables -A OUTPUT -d "$IPCliente2" -j ACCEPT
elif [ "$MAQUINA_ATUAL" = "cliente2" ]; then
    iptables -A OUTPUT -d "$IPCliente1" -j ACCEPT
    iptables -A OUTPUT -d "$IPCliente3" -j ACCEPT
elif [ "$MAQUINA_ATUAL" = "cliente3" ]; then
    iptables -A OUTPUT -d "$IPCliente4" -j ACCEPT
    iptables -A OUTPUT -d "$IPCliente2" -j ACCEPT
elif [ "$MAQUINA_ATUAL" = "cliente4" ]; then
    iptables -A OUTPUT -d "$IPCliente3" -j ACCEPT
    iptables -A OUTPUT -d "$IPCliente5" -j ACCEPT
elif [ "$MAQUINA_ATUAL" = "cliente5" ]; then
    iptables -A OUTPUT -d "$IPCliente0" -j ACCEPT
    iptables -A OUTPUT -d "$IPCliente4" -j ACCEPT
    

# # Adicionar a regra para bloquear o tráfego de saída para a rede 192.168.60.0/24
# iptables -A OUTPUT -s "$LOCAL_IP" -d 192.168.60.0/24 -j ACCEPT

# # Permitir tráfego de saída do host local para a rede 192.168.60.0/24
# iptables -A OUTPUT -s "$LOCAL_IP" -d 192.168.60.0/24 -j ACCEPT

# # Bloquear tráfego de saída de outros hosts na rede 192.168.60.0/24 para outros hosts na mesma rede
# iptables -A OUTPUT -s 192.168.60.0/24 -d 192.168.60.0/24 ! -o lo -j DROP