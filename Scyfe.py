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

from tests import *
from client import *
from server import *


#major functionality
def runAsClient(serverIp, label):
    pass

def runAsServer(serverIp):
    pass

def runStubbedClient(serverIp, label):
    pass

def runStubbedServer(serverIp, label):
    pass


#def local testing
def runLocalTests():
    pass

if __name__ == "__main__":
    runLocalTests()

    #runAsClient()
    #runAsServer()
    #runStubbedClient()
    #runStubbedServer()

    #Chlorine- threading, pool and task management
    #Relay- sockets, streams, buffering
    #Dispatch- routing and addressing
    #Slander- threat detection and gossip network implementation