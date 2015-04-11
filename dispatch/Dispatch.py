'''
Routing.
'''

from utils import *

fname = "Dispatch"

class Dispatch:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent

    #Given a client, resolve the clients IP address
    def resolveClient(self, client):
        pass

    # Given a client, resolve the route to the client and return the next-hop client
    # returns- clientId to the next client in the route 
    def nextHop(self, client):
        pass
