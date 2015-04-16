'''
A static (no group reconfiguration) test using processes.

Classic client/server architecture. 
'''

from multiprocessing import Process
import os

from utils import *

def run(numClients):
    print("running Process Test")

    server = Process(target = startServerProcess)
    server.start()

    clients = []

    for i in range(0, 3):
        clientProcess = Process(target = startClientProcess)
        clientProcess.start()
        clients.append(clientProcess)

    server.join()


def startClientProcess():
    import ServerMock
    client = ClientMock.ClientMock(name)
    client.connect('127.0.0.1', 40000)

def startServerProcess():
    import ClientMock
    server = ServerMock.ServerMock()
    server.start("127.0.0.1")


def serverTest():
    addr = 'localhost'
    port = 777

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((addr, port))
    sock.listen(5)

    while True:
        connection, client_address = sock.accept()
        data = connection.recv(1024)
        print(client_address)
        print(data)
        connection.close()

def clientTest():
    addr = 'localhost'
    port = 777

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (serverIp, serverPort)
    sock.connect(server_address)
    sock.sendall("This is the message")
    sock.close()

