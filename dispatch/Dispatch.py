'''
Routing.
'''

from utils import *

fname = "Dispatch"

class Dispatch:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent