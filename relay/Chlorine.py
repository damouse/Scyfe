'''
Multitasking and Threading.

Used to process tasks from the entirity of the application. 
'''

from utils import *
from relay import NetworkFunctions

import select 
import socket 
import sys 
import threading 


class Chlorine:
    #Requires a reference to its parent. Directly accesses other modules on the parent
    def __init__(self, parent):
        self.name = "Chlorine"
        self.parent = parent
        self.workers = []
        self.poolSize = 10

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret

    def openConnection(self, sockinfo):
        worker = ConnectionThread(sockinfo, self.parent)
        self.workers.append(worker)
        worker.start()

    #terminate all connections, join all worker threads, and return
    def kill(self):
        Utils.log(self.name, "Closing worker threads...")
        for worker in self.workers:
            worker.close()

        for worker in self.workers:
            worker.join()

        Utils.log(self.name, "All threads closed, done.")

''' Represents a connection to a remote client or server '''
class ConnectionThread(threading.Thread): 
    def __init__(self, (client, address), parent): 
        threading.Thread.__init__(self) 
        self.name = "WorkerThread"

        Utils.dlog(self.name, "Worker Init: " + str(client) + " " + str(address))

        self.client = client 
        self.address = address 
        self.size = 4096 
        self.parent = parent #client or server instance
        self.running = False

    def run(self):
        Utils.log(self.name, "Worker thread started")

        running = True 

        while running: 
            data = None
            data = NetworkFunctions.recv_msg(self.client)

            # try: 
            #     data = NetworkFunctions.recv_msg(self.client)
            # except Error as e: 
            #     Utils.log(self.name, "WARN-- exception when processing the data: " + str(e))
            #     self.parent.hcf()
            #     return

            Utils.log(self.name, "Received message")

            if data: 
                self.parent.handleMessage(data)
            else: 
                #inform parent the connection was closed remotely
                self.client.close() 
                running = False

    def send(self, message):
        self.client.send(message)

    def close(self):
        self.running = False
        self.client.close()