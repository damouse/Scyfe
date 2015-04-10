'''
Entry point for server-side module. 
'''

import sys
from utils import *

fname = 'Server'

class Server:
    def __init__(self, label):
        self.label = label

    #Make this server sound off indicating it is alive. 
    #TODO: log the server IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(fname, 'Server named: ' + self.label)
