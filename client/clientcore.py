'''
Entry point for client-side module. 
'''

import sys
from utils import *

fname = 'Main'

class Client:
    def __init__(self, label):
        self.label = label

    #Make this client sound off indicating it is alive. 
    #TODO: log the clients IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(fname, 'Client named: ' + self.label)


if __name__ == "__main__":
    client = Client('Test')
    client.soundOff()