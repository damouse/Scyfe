'''
Entry point for server-side module. 
'''

from frontend import Peer, RemotePeer

class Server(Peer.Peer):
    def __init__(self, label, application):
        Peer.Peer.__init__(self, label, application)