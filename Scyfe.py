
'''
Entry point for Scyfe functionality. 

This file exectures the rest of the project and can be run in three ways:
    -Server
    -Client
    -Tests

The first two run this instance as given, while the third either runs local tests
verifying project functionality or wraps a client/server instance as a mock (most likely
pretending to be an application implementation.)
'''
import sys
from multiprocessing import Process
import os

from tests import *
from utils import Utils

fname = 'Main'

basePort = 7778
baseAddr = '127.0.0.1'

#major functionality
def runAsClient(serverIp, label):
    pass

def runAsServer(serverIp):
    pass

def runStubbedClient(serverIp, label):
    client = ClientMock.ClientMock(label)
    client.connect(serverIp, basePort)

def runStubbedServer():
    server = ServerMock.ServerMock()
    server.start(baseAddr, basePort)

#testing live local simualtion
def runSimulation():
    server = Process(target = runStubbedServer)
    client = Process(target = runStubbedClient, args = ('127.0.0.1', 'TestClient'))

    server.start()
    client.start()

    server.join()
    client.join()

#development tests
def runLocalTests():
    Utils.log(fname, 'Starting all tests')

    Stable.runTests()

    Utils.log(fname, 'All Tests Completed')


if __name__ == "__main__":
    # runLocalTests()
    # runSimulation()

    #runAsClient()
    #runAsServer()

    serverOrClient = sys.argv[1]
    if(serverOrClient == 'c'):
        runStubbedClient('127.0.0.1', 40000)
    else:
        runStubbedServer()

