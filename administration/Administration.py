'''
Top level protocol management. 

This file defines all the possible administrative protocol actions. 

Types of messages
    Group
        join, leave, handshake
    Keys
        keyswap, keyask
    Variables
        change, validate, propogate
'''

from utils import *
from relay import Message

fname = "Administration"

class Administration:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent 
        self.variables = []
        self.groupId = None
        self.groupies = []

        #area of interest
        self.subscriptions = []

    def setGroup(self, groupUpdateMessage):
        self.groupId = groupUpdateMessage.groupId

        #remove old connections!

        #connect to new peers
        self.groupies = groupUpdateMessage.peers

        #remove subscriptions? Likely not.

        #handshake with the new groupies-- assumes no changes in group!
        for peer in self.groupies:
            self.parent.relay.connect(peer)
            self.parent.relay.send(peer, Message.GroupHandshake(self.variables, self.parent.id))

        Utils.dlog(self.parent.id, "Changed group to " + str(self.groupId))

    def acceptGroupHandshake(self, groupHandshakeMessage, peer):
        #if you do this then all group changes have to be managed by the server!
        if not peer in self.groupies:
            Utils.log(fname, "WARN-- group handshaking on a peer that does not exist in the groupies!")
            return None

        groupie = [x for x in self.groupies if x.id == groupHandshakeMessage.id][0]
        if not groupie.readGroupHandshake(groupHandshakeMessage):  
            self.parent.relay.send(peer, Message.GroupHandshake(self.variables, self.parent.id))

    #called from the server with an updated list of variables for this client
    def addVariable(self, variableMessage):
        Utils.dlog(self.parent.id, "Added variable " + str(variableMessage.variable.name))

        self.variables.append(variableMessage.variable)
