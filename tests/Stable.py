'''
All relevant classes can be instantiated without crashing and project 
is in a stable state with regards to configuration
'''

import sys
from utils import *
from client import *
from server import *


def stable():
    Utils.log('Test.Stable', 'testing instantiation of all objects')
    client = ClientCore.Client("TestClient")
    client.soundOff()

def runTests():
    stable()
