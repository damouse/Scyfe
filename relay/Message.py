from utils import *

class Handshake:
    def __init__(self, groupId, senderId):
        self.group = groupId
        self.id = senderId

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

# A peer just joined a group. Give them a record of our variables
class GroupHandshake:
    def __init__(self, variables, peerId):
        self.id = peerId
        self.variables = variables

# A dummy message used to test message handoffs
class TestMessage:
    def __init__(self, num):
        self.values = []

        for i in range(0, num):
            self.values.append(i)

    def __repr__(self):
        return "TestMessage: " + str(len(self.values))

class LabeledPing: 
    def __init__(self, name):
        self.recipient = ""
        self.sender = name

    def __repr__(self):
        return "LabeledPingMessage: " + self.sender + " to " + self.recipient