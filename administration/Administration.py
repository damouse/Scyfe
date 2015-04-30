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

        #remove old connections
        #connect to new peers
        self.groupies = groupUpdateMessage.peers

        #remove subscriptions? Likely not.

        Utils.dlog(self.parent.id, "Changed group to " + str(self.groupId))

    #called from the server with an updated list of variables for this client
    def addVariable(self, variableMessage):
        Utils.dlog(self.parent.id, "Added variable " + str(variableMessage.variable.name))

        self.variables.append(variableMessage.variable)




