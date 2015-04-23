'''
Network connections and messages. 

Establishes connections, sends packets. Arguments for targets are the actual objects
and not IP addresses-- these should be contained within the targets. 

Note that "target" can refer to a client or a server-- they both have a field that identifies their IP address
'''

from utils import *
from relay import NetworkFunctions
from relay import TestMessage

import select 
import socket 
import sys 

import pickle
import struct


class Relay:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.name = "Relay"
        self.parent = parent
        self.openSocket = None
        self.relayOpen = False


    #Open the relay for communication
    def open(self, addr, port):
        try: 
            self.openSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.openSocket.bind((addr, port)) 
            self.openSocket.listen(5) 

        except socket.error, (value,message): 
            if self.openSocket: 
                self.openSocket.close() 
            Utils.log(self.name, "Could not open socket: " + message)
            sys.exit(1) 

        sockIn = [self.openSocket] 
        self.relayOpen = True 

        while self.relayOpen: 
            inputready, outputready, exceptready = select.select(sockIn,[],[]) 

            if not self.relayOpen: 
                Utils.log(self.name, "Relay received a message after being closed. Ignoring the message")
                return

            Utils.dlog(self.name, "Received something " + str(inputready))
            for s in inputready: 
                if s == self.openSocket: 
                    self.parent.handleConnection(self.openSocket.accept())
                else:
                    Utils.log(self.name, "WARN-- received something not considered to be a socket")

    #end communication through this relay. Note-- does not close worker threads
    def close(self):
        self.openSocket.close()
        self.relayOpen = False


    # Opens a connection to a given entity
    def connect(self, target):
        pass

    # Send a message to a target. Assumes a connection has already been opened with the target. 
    def send(self, target, message):
        pass

    def TEST(self, addr, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))

        packet = TestMessage.TestMessage(1000)
        NetworkFunctions.send_msg(s, packet)

        Utils.log("RelayTesting", "Sent test message.")
        s.close()


    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret


