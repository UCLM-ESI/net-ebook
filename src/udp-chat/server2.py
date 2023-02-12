#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("", 12345))

msg, client = sock.recvfrom(1024)
print(f"{msg.decode()} from {client}")

sock.sendto("hi there".encode(), client)

sock.close()
