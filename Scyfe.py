
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

from time import sleep
import time

fname = 'Main'

basePort = 7836
baseAddr = '127.0.0.1'

#major functionality
def runAsClient(serverIp, label):
    pass

def runAsServer(serverIp):
    pass

def runStubbedClient(addr, port, label):
    client = ClientMock.ClientMock(label)
    client.start(addr, port, baseAddr, basePort)

def runStubbedServer():
    server = ServerMock.ServerMock()
    server.start(baseAddr, basePort)

#testing live local simualtion
def runSimulation():
    server = Process(target = runStubbedServer)
    client = Process(target = runStubbedClient, args = (baseAddr, basePort + 1, "Test Client"))

    server.start()
    sleep(1)
    client.start()

    # server.join()
    # client.join()

    sleep(2)
    server.terminate()
    client.terminate()

#development tests
def runLocalTests():
    Utils.log(fname, 'Starting tests')
    Stable.runTests()


if __name__ == "__main__":
    # runLocalTests()
    runSimulation()

    #runAsClient()
    #runAsServer()

    #runStubbedClient(baseAddr, basePort, "Test Client")
    #runStubbedServer()