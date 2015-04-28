'''
Entry point for client-side module. 
'''

from frontend import Peer as Peer


class Client(Peer.Peer):
    def __init__(self, label, application):
        Peer.Peer.__init__(self, label, application)