'''
A wrapper meant to mimic the server application relying on this library to function. 

This wrapper interfaces with the ServerCore object and pretends to be a normal server.
'''

from utils import *
from client import ClientCore

class ClientMock:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, name):
        self.name = name + " wrapper"
        self.client = ClientCore.Client(name, self)

    def connect(self, ipAddress):
        Utils.dlog(self.name, "Client connecting")
        
        self.client.connect(ipAddress)