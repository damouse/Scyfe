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

        self.workers = []
        self.poolSize = 10

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
        Utils.log(self.name, "Closing worker threads...")
        for worker in self.workers:
            worker.close()

        self.relayOpen = False
        for worker in self.workers:
            worker.join()

        Utils.log(self.name, "All threads closed, done.")

        self.listener.join()

    # Opens a connection to a given entity
    def acceptConnection(self, sockinfo):
        worker = ConnectionThread(self.parent, sockinfo, None)
        self.workers.append(worker)
        worker.start()
        worker.listen()

    def connect(self, addr, port):
        worker = ConnectionThread(self.parent, (None, addr), port)
        self.workers.append(worker)
        worker.start()

    def disconnect(self, target):
        pass

    # Send a message to a target. Assumes a connection has already been opened with the target. 
    def send(self, addr, port, message):
        worker = [x for x in self.workers if x.addr == addr and x.port == port][0]
        worker.send(message)

    def TEST(self, addr, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))

        packet = TestMessage.TestMessage(1000)
        NetworkFunctions.send_msg(s, packet)

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
            inputready, outputready, exceptready = select.select(sockIn,[],[], self.timeout) 

            if not self.relay.relayOpen: 
                sock.close()
                return

            for s in inputready: 
                if s == sock: 
                    self.parent.handleConnection(sock.accept())


''' Represents a connection to a remote client or server '''
class ConnectionThread(threading.Thread): 
    def __init__(self, parent, (client, addr), port): 
        threading.Thread.__init__(self) 
        self.name = "WorkerThread"

        self.addr = addr 

        #if we are passed a socket then a connection has already been made
        if client is not None:
            self.socket = client 
        else:
            self.port = port
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((addr, port))

        self.size = 4096 
        self.parent = parent #client or server instance
        self.running = False

    def run(self):
        pass

    def listen(self):
        Utils.log(self.name, "Worker thread started")
        running = True 

        while running: 
            data = None
            data = NetworkFunctions.recv_msg(self.socket)

            Utils.dlog(self.name, "Received message")

            if data: 
                self.parent.handleMessage(data)
            else: 
                #inform parent the connection was closed remotely
                self.socket.close() 
                running = False

    def send(self, message):
        NetworkFunctions.send_msg(self.socket, message)

    def close(self):
        self.running = False
        self.socket.close()