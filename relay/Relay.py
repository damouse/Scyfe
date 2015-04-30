'''
Network connections and messages. 

Establishes connections, sends packets. Arguments for targets are the actual objects
and not IP addresses-- these should be contained within the targets. 

Note that "target" can refer to a client or a server-- they both have a field that identifies their IP address

See here for a better implementation of the multi-connection architecture using 
select: http://code.activestate.com/recipes/531824-chat-server-client-using-selectselect/

And P2P chat: http://code.activestate.com/recipes/578591-primitive-peer-to-peer-chat/

Twisted and Kademlia: http://entangled.sourceforge.net/
'''

from utils import *
from relay import NetworkFunctions
from relay import Message
from frontend import RemotePeer

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
        self.listener = RelayListener(self.parent, 1, addr, port, self)

        self.listener.start()

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
    def acceptConnection(self, peer):
        worker = ConnectionThread(self.parent, peer)
        self.workers.append(worker)

        worker.send(Message.Handshake(self.parent.administration.groupId, self.parent.id))

    def connect(self, peer):
        worker = ConnectionThread(self.parent, peer)
        self.workers.append(worker)

    def disconnect(self, peer):
        pass

    # Send a message to a target. Assumes a connection has already been opened with the target. 
    def send(self, peer, message):
        worker = [x for x in self.workers if x.peer == peer][0]
        worker.send(message)

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
        Utils.log(self.name, "Listener binding to " + self.addr + ":" + str(self.port))

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
                    sock, portinfo = sock.accept()
                    addr, port = portinfo

                    peer = RemotePeer.RemotePeer(addr, port)
                    peer.sock = sock
                    self.parent.handleConnection(peer)


''' Represents a connection to a remote client or server '''
class ConnectionThread: 
    def __init__(self, parent, peer): 
        self.name = "WorkerThread"
        self.addr = peer.addr 
        self.peer = peer

        #if we are passed a socket then a connection has already been made
        if peer.sock is not None:
            self.socket = peer.sock 
        else:
            self.port = peer.port
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((peer.addr, peer.port))

        self.size = 4096 
        self.parent = parent #client or server instance
        self.running = False

        #start listening thread
        self.thread = threading.Thread(target = self.listen)
        self.thread.start()

    def listen(self):
        self.running = True 

        while self.running: 
            data = None
            data = NetworkFunctions.recv_msg(self.socket)

            if data: 
                self.parent.handleMessage(data, self.peer)
            else: 
                self.close() 
                self.parent.connectionLost(self.peer)

    def send(self, message):
        NetworkFunctions.send_msg(self.socket, message)

    def close(self):
        self.running = False
        self.thread.stop()
        self.socket.close()
