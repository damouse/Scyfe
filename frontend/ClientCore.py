'''
Entry point for client-side module. 
'''

from frontend import Peer as Peer
from relay import *
from utils import *

class Client(Peer.Peer):
    def __init__(self, label, application):
        Peer.Peer.__init__(self, label, application)


    ''' Lifecycle management '''
    #Start the listener with the given address and port
    def start(self, addr, port, serverAddr, serverPort):
        thread = Peer.Peer.start(self, addr, port)

        #relay open, connect to the server and receive starting data
        #TESTING
        self.saddr = serverAddr
        self.sport = serverPort

        self.relay.connect(self.saddr, self.sport)

        return thread

    def test(self):
        self.relay.connect(self.saddr, self.sport)

        test = TestMessage.TestMessage(100)
        self.relay.send(self.saddr, self.sport, test)