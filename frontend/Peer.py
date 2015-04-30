'''
Base class for client and server instances. covers the functionality shared by both. 
'''

import sys
import socket
import threading 

from utils import *
from administration import *
from dispatch import *
from notary import *
from relay import *
from slander import *


class Peer:
    def __init__(self, label, application):
        self.id = label #random, non-colliding string
        self.application = application

        self.running = False
        self.spinWaitThread = None

        #all peers, not just the ones in the group
        self.peers = []

        #Modules
        self.relay = Relay.Relay(self)
        self.administration = Administration.Administration(self)
        self.notary = Notary.Notary(self)
        self.slander = Slander.Slander(self)
        self.dispatch = Dispatch.Dispatch(self)


    ''' Lifecycle management '''
    #Start the listener with the given address and port
    def start(self, addr, port):
        Utils.log(self.id, "Started client")

        self.running = True
        self.relay.open(addr, port)

        self.spinWaitThread = threading.Thread(target = self.mainSpinLoop)
        self.spinWaitThread.start()

        return self.spinWaitThread

    #Close the relay, disconnect gracefully, informing all peers and clients of the change
    def stop(self):
        self.running = False

    def mainSpinLoop(self):
        while self.running:
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
    def handleMessage(self, message, peer):
        # Utils.dlog(self.id, "Received type: " + str(message.__class__))
        Utils.dlog(self.id, "Received [" + str(message.__class__) + "] from [" + str(peer.id) + "]")


        if isinstance(message, Message.VariableAssignment):
            self.administration.addVariable(message)

        elif isinstance(message, Message.GroupAssignment):
            self.administration.setGroup(message)

        elif isinstance(message, Message.Handshake):
            if peer.readHandshake(message):
                self.relay.send(peer, Message.Handshake(self.administration.groupId, self.id))

        else:
            Utils.log(self.id, "WARN-- received message of type: " + str(message) + ", don't know how to handle!")
            return None

    #handle a newly created connection
    def handleConnection(self, peer):
        self.relay.acceptConnection(peer)
        self.peers.append(peer)

    def connectionLost(self, peer):
        self.peers.remove(peer)

    ''' Utilities and Bookeeping '''
    #Make this client sound off indicating it is alive. 
    #TODO: log the clients IP address and any other relevant information (#packets, etc)
    def soundOff(self):
        Utils.log(self.id, 'Hello. I am a client.')

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret