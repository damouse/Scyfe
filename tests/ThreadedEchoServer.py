#!/usr/bin/env python 

""" 
An echo server that uses threads to handle multiple clients at a time. 
Entering any line of input at the terminal will exit the server. 
""" 

import select 
import socket 
import sys 
import threading 
import pickle

import struct

class TestObject:
    def __init__(self, num):
        self.values = []

        for i in range(0, num):
            self.values.append(i)

    def __repr__(self):
        return "" + str(self.values)

class Server: 
    def __init__(self): 
        self.host = '127.0.0.1' 
        self.port = 7809 
        self.backlog = 5 
        self.size = 4096 
        self.server = None 
        self.threads = [] 

    def open_socket(self): 
        try: 
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.server.bind((self.host, self.port)) 
            self.server.listen(5) 
        except socket.error, (value,message): 
            if self.server: 
                self.server.close() 
            print "Could not open socket: " + message 
            sys.exit(1) 

    def run(self): 
        self.open_socket() 
        input = [self.server] 
        # input = [self.server, sys.stdin] 
        running = 1 
        while running: 
            inputready, outputready, exceptready = select.select(input,[],[]) 

            for s in inputready: 

                if s == self.server: 
                    # handle the server socket 
                    c = Client(self.server.accept()) 
                    c.start() 
                    self.threads.append(c) 

                    #TEMP
                    for c in self.threads: 
                        c.join()

                    self.server.close() 
                    sys.exit(0)

                elif s == sys.stdin: 
                    # handle standard input 
                    junk = sys.stdin.readline() 
                    running = 0 

        # close all threads 

        self.server.close() 
        for c in self.threads: 
            c.join() 

class Client(threading.Thread): 
    def __init__(self,(client,address)): 
        threading.Thread.__init__(self) 
        self.client = client 
        self.address = address 
        self.size = 1024 

    def run(self): 
        running = 1 
        while running: 
            # data = self.client.recv(self.size) 
            data = recv_msg(self.client)

            if data: 
                self.client.send(data)

                #TEMP-- close right away 
                print data
                unpick = pickle.loads(data)
                print unpick
                self.client.close()
                sys.exit(0)
            else: 
                self.client.close() 
                running = 0 

def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None

    msglen = struct.unpack('>I', raw_msglen)[0]
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


if __name__ == "__main__": 
    s = Server() 
    s.run()