'''
Multitasking and Threading.

Used to process tasks from the entirity of the application. 
'''

from utils import *

fname = "Chlorine"

class Chlorine:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent