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


''' Messages '''

#assignment of a variable from the server
class VariableAssignment:
    def __init__(self, variable):
        self.variable = variable
        self.key = None #auth key