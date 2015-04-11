'''
Entry point for server-side module. 
'''

import sys
from utils import *
from administration import *
from chlorine import *
from dispatch import *
from notary import *
from relay import *
from slander import *

class Server:
    def __init__(self, label, application):
        self.id = label #random, non-colliding string
        self.label = label
        self.variables = []
        self.clients = []
        self.application = application

        #Modules
        self.relay = Relay.Relay(self)
        self.administration = Administration.Administration(self)
        self.chlorine = Chlorine.Chlorine(self)
        self.notary = Notary.Notary(self)
        self.slander = Slander.Slander(self)
        self.dispatch = Dispatch.Dispatch(self)

    #Start listening and be ready to accept clients
    #Depending on implementation, may want to read all existing client variables here
    def start(self):
        pass

    #create Variable for clients 
    def createVariable(self):
        pass


    ''' Application Interface '''
    def clientConnected(self):
        pass

    def clientDisconnected(self):
        pass


    ''' Utilities and Bookeeping '''
    #Make this client sound off indicating it is alive. 
    #TODO: log the clients IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(self.id, 'Hello. I am a server.')

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret