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

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret


class Worker(threading.Thread): 
    def __init__(self, (target, address)): 
        threading.Thread.__init__(self) 
        self.target = target 
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