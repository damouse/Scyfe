
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
from utils import *

fname = 'Main'


#major functionality
def runAsClient(serverIp, label):
    pass

def runAsServer(serverIp):
    pass

def runStubbedClient(serverIp, label):
    pass

def runStubbedServer(serverIp, label):
    pass


#development tests
def runLocalTests():
    Utils.log(fname, 'Starting all tests')

    Stable.runTests()

    Utils.log(fname, 'All Tests Completed')


if __name__ == "__main__":
    runLocalTests()

    #runAsClient()
    #runAsServer()
    #runStubbedClient()
    #runStubbedServer()