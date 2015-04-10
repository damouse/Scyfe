'''
Entry point for server-side module. 
'''

import sys
from utils import *

class Server:
    def __init__(self, label):
        self.id = label

    #Make this server sound off indicating it is alive. 
    #TODO: log the server IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(self.id, 'Hello. I am a server.')
