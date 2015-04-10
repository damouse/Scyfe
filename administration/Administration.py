'''
Top level protocol management. 

This file defines all the possible administrative protocol actions. 
'''

from utils import *

fname = "Administration"

class Administration:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent