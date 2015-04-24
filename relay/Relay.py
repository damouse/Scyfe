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
import threading 


class Relay:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.name = "Relay"
        self.parent = parent
        self.openSocket = None
        self.relayOpen = False

        self.listener = None


    #Open the relay for communication
    def open(self, addr, port):
        self.relayOpen = True
        Utils.dlog(self.name, "Starting Thread")
        self.listener = RelayListener(self.parent, 1, addr, port, self)

        self.listener.start()

        #this is here so the program doesn't complete and for no other reason-- should make a spin in parent
        self.listener.join()

    #end communication through this relay. Note-- does not close worker threads
    def close(self):
        self.relayOpen = False
        self.listener.join()

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

'''
A threaded wrapper around the listening blocking call. 

This thread listens for incoming connections and passes new conncetions to the parent 
to handle on receive. It polls for a suicide flag every n seconds. 
'''
class RelayListener(threading.Thread):
    def __init__(self, parent, timeout, addr, port, relay):
        threading.Thread.__init__(self) 
        self.name = "Relay Listener"
        self.addr = addr
        self.port = port
        self.parent = parent
        self.timeout = timeout
        self.relay = relay

    def run(self):
        Utils.dlog(self.name, "Listener started")

        try: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            sock.bind((self.addr, self.port)) 
            sock.listen(5) 

        except socket.error, (value,message): 
            if sock: 
                sock.close() 
            Utils.log(self.name, "Could not open socket: " + message)
            sys.exit(1) 

        sockIn = [sock] 
        while self.relay.relayOpen:
            Utils.dlog(self.name, "Listening for connections...")
            inputready, outputready, exceptready = select.select(sockIn,[],[], self.timeout) 

            if not self.relay.relayOpen: 
                sock.close()
                return

            for s in inputready: 
                if s == sock: 
                    self.parent.handleConnection(sock.accept())

