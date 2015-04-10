'''
Validation management. 

Performs validation for operations on the local client as well as changes in state that occur on 
remote clients-- 
'''

from utils import *

fname = "Notary"

class Notary:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent