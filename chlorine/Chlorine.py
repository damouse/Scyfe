'''
Multitasking and Threading.

Used to process tasks from the entirity of the application. 
'''

from utils import *

import select 
import socket 
import sys 
import threading 

fname = "Chlorine"

class Chlorine:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.parent = parent
        self.workers = []
        self.poolSize = 10

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret

    #register with Relay, listening for new connections
    def listen(self):
        pass

    #terminate all connections, join all worker threads, and return
    def kill():
        pass


''' 
Represents a connection to a remote client or server
'''
class Worker(threading.Thread): 
    def __init__(self, (source, address)): 
        threading.Thread.__init__(self) 
        self.source = source 
        self.address = address 
        self.size = 1024 

    def run(self): 
        running = 1 
        while running: 
            data = self.target.recv(self.size) 
            if data: 
                self.target.send(data) 
            else: 
                self.target.close() 
                running = 0 