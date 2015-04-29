'''
An instance of a peer as seen by a remote connection
'''

class RemotePeer:
    def __init__(self, id, addr, port):
        self.id = id
        self.addr = addr
        self.port = port

        self.variables = []