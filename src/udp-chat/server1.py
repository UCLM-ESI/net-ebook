#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("", 12345))  # Con esta línea le decimos al socket que queremos usar el puerto 12345 para escuchar mensajes

message, client = sock.recvfrom(1024)  # El método devolvera una tupla con el mensaje recibido y la dirección del cliente. 1024 es el tamaño del buffer de recepción.

print(f"{message.decode()} from {client}")

sock.close()
