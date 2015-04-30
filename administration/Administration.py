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
        self.peers = []

        #area of interest
        self.subscriptions = []

    def setGroup(self, groupUpdateMessage):
        self.groupId = groupUpdateMessage.groupId

        #remove old connections
        #connect to new peers
        self.peers = groupUpdateMessage.peers

        #remove subscriptions? Likely not.

        Utils.dlog(self.parent.id, "Changed group to " + str(self.groupId))

    #called from the server with an updated list of variables for this client
    def addVariable(self, variableMessage):
        Utils.dlog(self.parent.id, "Added variable " + str(variableMessage.variable.name))

        self.variables.append(variableMessage.variable)


''' Messages '''
#assignment of a variable from the server
class VariableAssignment:
    def __init__(self, variable):
        self.variable = variable
        self.key = None #auth key

    def __repr__(self):
        return "VariableAssignment"

''' 
Assign the client to a new group. Included is a list of peers in this new group-- if empty then create
a new empty group (or assign to the server?)
'''
class GroupAssignment:
    def __init__(self, groupId):
        self.groupId = groupId
        self.peers = []

    def __repr__(self):
        return "VariableAssignment"