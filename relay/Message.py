'''
Abstraction of a packetized message. Subclass this to create actual messages. (?)
'''

from utils import *

class Message:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.id = "Message"

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret