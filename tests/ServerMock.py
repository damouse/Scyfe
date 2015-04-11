'''
A wrapper meant to mimic the server application relying on this library to function. 

This wrapper interfaces with the ServerCore object and pretends to be a normal server.
'''

from utils import *
from server import ServerCore

class ServerMock:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self):
        self.name = "ServerMock"
        self.server = ServerCore.Server("Server", self)

    def start(self,ipAddress):
        Utils.dlog(self.name, "Starting server")
        
        self.server.start(ipAddress)

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret