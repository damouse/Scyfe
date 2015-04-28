'''
A wrapper meant to mimic the client application relying on this library to function. 

This wrapper interfaces with the ClientCore object and pretends to be a normal server.
'''

from utils import *
from frontend import *

class ClientMock:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, name):
        self.name = name + " wrapper"
        self.client = ClientCore.Client(name, self)

    def start(self, addr, port, serverAddr, serverPort):
        Utils.dlog(self.name, "Client connecting")
        self.client.start(addr, port, serverAddr, serverPort)

        self.client.test()

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret


