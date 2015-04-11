'''
Entry point for server-side module. 
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

class Server:
    MAX_CONNECTIONS=5
    TCP_PORT=40000

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
    #Starts server on specified ipAddress
    def start(self,ipAddress):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ipAddress, self.TCP_PORT))
        sock.listen(self.MAX_CONNECTIONS)

        while True:
            connection, client_address = sock.accept()
            data = connection.recv(1024)
            print(client_address)
            print(data)
            connection.close()



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