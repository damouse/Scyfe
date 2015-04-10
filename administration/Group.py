'''
A group of clients
'''

from utils import *

fname = "Group"

class Group:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent
        self.members = []