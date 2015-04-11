'''
Validation management. 

Performs validation for operations on the local client as well as changes in state that occur on 
remote clients-- 
'''

from utils import *

fname = "Slander"

class Slander:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret