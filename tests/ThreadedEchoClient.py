#!/usr/bin/env python

import pickle
import struct
"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
   

class TestObject:
    def __init__(self, num):
        self.values = []

        for i in range(0, num):
            self.values.append(i)

    def __repr__(self):
        return "" + values

if __name__ == "__main__": 
    import socket
    import sys


    host = 'localhost'
    port = 7809
    size = 4096
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    packet = TestObject(1000)
    pickled = pickle.dumps(packet)
    send_msg(s, pickled)

    s.close()
