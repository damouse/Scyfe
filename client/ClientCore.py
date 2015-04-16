'''
Entry point for client-side module. 
'''

import sys
import socket

from utils import *
from administration import *
from chlorine import *
from dispatch import *
from notary import *
from relay import *
from slander import *

class Client:
    def __init__(self, label, application):
        self.id = label #random, non-colliding string
        self.label = label
        self.variables = []
        self.application = application

        #Modules
        self.relay = Relay.Relay(self)
        self.administration = Administration.Administration(self)
        self.chlorine = Chlorine.Chlorine(self)
        self.notary = Notary.Notary(self)
        self.slander = Slander.Slander(self)
        self.dispatch = Dispatch.Dispatch(self)

    #Connect to the server synchonously. Receive group assignments and default variables and values
    def connect(self, serverIp, serverPort):
        Utils.log(self.id, "Started client")
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (serverIp, serverPort)
        sock.connect(server_address)
        sock.sendall("This is the message")
        sock.close()

    def disconnect(self):
        pass


    ''' Application Interface '''
    #Given the variable (by name?) and an update to the variable, begin the validation process
    def inputValue(self, variable, update):
        pass

    #A variable changed. It could be on us or on another client. The application needs to be notified for the purpose of 
    #rendering
    def inputChanged(self, client, variable):
        Utils.dlog(self.id, "Alerting application of a validated variable change on client: " + client + " variable: " + variable)

    #We have successfully connected to the server
    def connectedToServer(self):
        Utils.dlog(self.id, "Connected to server")

        #inform the application

    #We were removed from the server (could be intentional or a kick)
    def disconnectedFromServer(self):
        Utils.dlog(self.id, "Disconnected from server")

        #inform the application


    ''' Packet Receiving and Processing '''
    # We have received a new packet. Figure out what to do with it.
    def handleMessage(self, message):
        pass


    ''' Utilities and Bookeeping '''
    #Make this client sound off indicating it is alive. 
    #TODO: log the clients IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(self.id, 'Hello. I am a client.')

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret