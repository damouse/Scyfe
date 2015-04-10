import sys

'''
All relevant classes can be instantiated without crashing and project 
is in a stable state with regards to configuration
'''

from utils import utils as Utils
import clientcore as ClientCore

def stable():
    Utils.log('Test.Stable', 'testing instantiation of all objects')
    client = ClientCore.Client("TestClient")
    client.soundOff()
    print 'Test:Stable-- success'

def testUtils():
    Utils.log('Test.Stable', "Logging works")

def runTests():
    stable()
    testUtils()
