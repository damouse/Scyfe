'''
Entry point for server-side module. 
'''

import sys
import socket

from utils import *
from administration import *
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


    ''' Lifecycle '''
    #Start listening and be ready to accept clients
    #Depending on implementation, may want to read all existing client variables here
    #Starts server on specified ipAddress
    def start(self, addr, port):
        self.relay.open(addr, port)

    # Close down shop.
    def stop(self):
        pass

    #An error or kick has occured. Shut everything down. Do not pass go. 
    def hcf(self):
        Utils.log(self.id, "WARN-- HFC called!")

        #self.chlorine.kill()
        #self.relay.close()


    #create Variable for clients 
    def createVariable(self):
        pass


    ''' Application Interface '''
    def clientConnected(self):
        pass

    def clientDisconnected(self):
        pass


    ''' Packet Receiving and Processing '''
    # We have received a new packet. Figure out what to do with it.
    def handleMessage(self, message):
        Utils.log(self.id, "Message Received")
        print message
        # self.hcf()

    #handle a newly created connection
    def handleConnection(self, sockInfo):
        Utils.log(self.id, "Connection Received")
        self.chlorine.openConnection(sockInfo)


    ''' Utilities and Bookeeping '''
    #Make this client sound off indicating it is alive. 
    #TODO: log the clients IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(self.id, 'Hello. I am a server.')

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret