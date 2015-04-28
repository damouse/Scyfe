'''
Entry point for client-side module. 
'''

import sys
import socket

from utils import *
from administration import *
from dispatch import *
from notary import *
from relay import *
from slander import *

class Client:
    def __init__(self, label, application):
        self.id = label #random, non-colliding string
        self.variables = []
        self.application = application

        self.group = None

        #Modules
        self.relay = Relay.Relay(self)
        self.administration = Administration.Administration(self)
        self.notary = Notary.Notary(self)
        self.slander = Slander.Slander(self)
        self.dispatch = Dispatch.Dispatch(self)


    ''' Lifecycle management '''
    #Connect to the server synchonously. Receive group assignments and default variables and values
    def connect(self, addr, port):
        Utils.log(self.id, "Started client")

        self.relay.connect(addr, port)

        test = TestMessage.TestMessage(100)
        self.relay.send(addr, port, test)

    #Close the relay, disconnect gracefully, informing all peers and clients of the change
    def disconnect(self):
        pass

    #An error or kick has occured. Shut everything down. Do not pass go. 
    def hcf(self):
        Utils.log(self.id, "WARN-- HFC called!")

        self.chlorine.kill()
        self.relay.close()


    ''' Application Interface '''
    #Given the variable (by name?) and an update to the variable, begin the validation process
    def inputValue(self, variable, update):
        pass

    #A variable changed. It could be on us or on another client. The application needs to be notified for the purpose of 
    #rendering
    def inputChanged(self, client, variable):
        Utils.dlog(self.id, "Alerting application of a validated variable change on client: " + client + " variable: " + variable)

    #Application notification-- a message has been received the app is likely interested in
    def alertApplication(self, message):
        pass


    ''' Packet Receiving and Processing '''
    # We have received a new packet. Figure out what to do with it.
    def handleMessage(self, message):
        Utils.log(self.id, "Message Received")
        print message

    #handle a newly created connection
    def handleConnection(self, sockInfo):
        self.relay.acceptConnection(sockInfo, self)


    ''' Utilities and Bookeeping '''
    #Make this client sound off indicating it is alive. 
    #TODO: log the clients IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(self.id, 'Hello. I am a client.')

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret