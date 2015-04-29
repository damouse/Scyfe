'''
A variable under supervision by Scyfe at large. 

Each client should have their own version of each variable object. Clients
are interested in each other's variables for the purposes of rendering. 


I don't know if i like the way this is sketched out, there may be a better way to 
do this-- have the application handle this itself.
'''

from utils import *

class Variable:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent, name, defaultValue):
        self.parent = parent
        self.name = name
        self.value = defaultValue

        #should this be considered a proximity variable-- that is, does this variable
        #tell us anything about the proximity of clients?
        self.proximity = False

        self.constraints = []

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret

class Update:
    def __init__(self, owner, oldVariable, newVariable):
        self.owner = owner
        self.name = oldVariable.name
        self.oldVariable = oldVariable
        self.newVariable = newVariable

        #Signatures and hashes?