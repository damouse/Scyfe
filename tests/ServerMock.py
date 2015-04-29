'''
A wrapper meant to mimic the server application relying on this library to function. 

This wrapper interfaces with the ServerCore object and pretends to be a normal server.
'''

from utils import *
from frontend import *
from administration import *

class ServerMock:
    def __init__(self):
        self.name = "ServerMock"
        self.server = ServerCore.Server("Server", self)

        self.createVariables()

    def createVariables(self):
        variables = []

        variables.append(Variable.Variable(None, "coordinate", [0, 0, 0]))
        variables.append(Variable.Variable(None, "currency", 0))
        variables.append(Variable.Variable(None, "health", 100))

    def start(self, ipAddress, port):
        Utils.dlog(self.name, "Starting server")
        thread = self.server.start(ipAddress, port)

        thread.join()

    def validateVariable(self, update):
        if update.name == "coordinate":
            return True

        if update.name == "currency":
            return True
            
        if update.name == "health":
            return True

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret