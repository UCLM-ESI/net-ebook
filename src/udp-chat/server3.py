#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_DGRAM

QUIT = b"bye"
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("", 12345))

while True:
    message_in, peer = sock.recvfrom(1024)
    print(message_in.decode())

    if message_in == QUIT:
        break

    message_out = input().encode()
    sock.sendto(message_out, peer)

    if message_out == QUIT:
        break

sock.close()
