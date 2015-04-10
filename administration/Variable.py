'''
A variable under supervision by Scyfe at large. 

Each client should have their own version of each variable object. Clients
are interested in each other's variables for the purposes of rendering. 
'''

from utils import *

fname = "Variable"

class Variable:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent, name, defaultValue):
        self.parent = parent
        self.name = name
        self.defaultValue = defaultValue

        self.constraints = []

    #define the permissible set of actions that can be performed on this variable
    def setConstraints(self):
        pass

    #change this variable as prescribed by the given delta, subject to constraints
    #return true/false if valid?
    def changeVariableDelta(self):
        pass