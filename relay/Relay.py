'''
Network connections and messages. 

Establishes connections, sends packets. Arguments for targets are the actual objects
and not IP addresses-- these should be contained within the targets. 

Note that "target" can refer to a client or a server-- they both have a field that identifies their IP address
'''

from utils import *

fname = "Relay"

class Relay:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent
        self.connections = []

    # Opens a connection to a given entity
    def connect(self, target):
        pass

    #informs the entity that we are closing connection to them 
    def close(self, target):
        pass

    # Send a message to a target. Assumes a connection has already been opened with the target. 
    def send(self, target, message):
        pass

    # Bind to a socket and start listening. Calls up to parent on receipt
    def listen(self):
        self.parent.handleMessage("This is a fake message")

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret