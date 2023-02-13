#!/usr/bin/env python3

"""usage: %s [--server|--client]"""

import sys
import socket
import threading


SERVER = ('', 12345)
QUIT = b'bye'


class Chat:
    """Represent a chat peer."""
    def __init__(self, sock, peer):
        self.sock = sock
        self.peer = peer

    def run(self):
        """Execute the chat logic."""
        threading.Thread(target=self.sending, daemon=True).start()
        self.receiving()
        self.sock.close()

    def sending(self):
        """Run a loop for reading messages from input and send them to the other peer."""
        while True:
            message = input().encode()
            self.sock.sendto(message, self.peer)

            if message == QUIT:
                break

    def receiving(self):
        """Run a loop for receiving messages from the peer and printing them."""
        while True:
            message, peer = self.sock.recvfrom(1024)
            print("other> {}".format(message.decode()))

            if message == QUIT:
                self.sock.sendto(QUIT, self.peer)
                break


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__ % sys.argv[0])
        sys.exit(1)

    mode = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if mode == '--server':
        sock.bind(SERVER)
        message, client = sock.recvfrom(0, socket.MSG_PEEK)
        Chat(sock, client).run()

    else:
        Chat(sock, SERVER).run()
