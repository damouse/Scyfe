'''
An instance of a peer as seen by a remote connection

If ID is none, the peer has not yet identified itself. 
'''

class RemotePeer:
    def __init__(self, addr, port):
        self.id = None
        self.group = None

        self.sock = None
        self.addr = addr
        self.port = port

        self.variables = []

    #using a handshake, populate as much information as possible about this peer
    #returns true if this handshake is new information, else false
    def readHandshake(self, handshake):
        ret = False
        if self.id is None: ret = True

        self.id = handshake.id
        self.group = handshake.group

        return ret

    #as above, read and apply the handshake information. Returns true if this is new infromation
    #( and this a first-time handshake) and false otherwise
    def readGroupHandshake(self, handshake):
        ret = False
        if len(self.variables) == 0: ret = True

        self.variables = handshake.variables

        return ret

    def __eq__(self, other):
        if not isinstance(other, RemotePeer): return False
        return self.sock == other.sock and self.port == other.port