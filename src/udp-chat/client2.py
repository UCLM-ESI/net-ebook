#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

sock.sendto("Hello".encode(), ("localhost", 12345))

msg, server = sock.recvfrom(1024)
print(f"{msg.decode()} from {server}")

sock.close()
