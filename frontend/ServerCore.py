'''
Entry point for server-side module. 
'''

from frontend import Peer, RemotePeer

class Server(Peer.Peer):
    def __init__(self, label, application):
        Peer.Peer.__init__(self, label, application)

        #maintains a list of all the clients, not just the directly connected ones
        self.clients = []

    #handle a newly created connection
    def handleConnection(self, sockInfo):
        thread = Peer.Peer.handleConnection(self, sockInfo)
        
        sock, portinfo = sockInfo
        addr, port = portinfo

        self.clients.append(RemotePeer.RemotePeer(None, addr, port))

