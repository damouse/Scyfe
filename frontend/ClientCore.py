'''
Entry point for client-side module. 
'''

from frontend import Peer
from frontend import RemotePeer
from relay import *
from utils import *

class Client(Peer.Peer):
    def __init__(self, label, application):
        Peer.Peer.__init__(self, label, application)


    ''' Lifecycle management '''
    #Start the listener with the given address and port
    def start(self, addr, port, serverAddr, serverPort):
        thread = Peer.Peer.start(self, addr, port)

        server = RemotePeer.RemotePeer(serverAddr, serverPort)
        self.peers.append(server)
        self.relay.connect(server)

        return thread

    def test(self):
        return None