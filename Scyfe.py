'''
Entry point for Scyfe functionality. 

This file exectures the rest of the project and can be run in three ways:
    -Server
    -Client
    -Tests

The first two run this instance as given, while the third either runs local tests
verifying project functionality or wraps a client/server instance as a mock (most likely
pretending to be an application implementation.)
'''
import sys
from multiprocessing import Process
from simulations import Writer
import os

from tests import *
from utils import Utils
from simulations import Sims
from simulations import Graphs

from time import sleep
import time

fname = 'Main'

basePort = 7854
baseAddr = '127.0.0.1'

#major functionality
def runAsClient(serverIp, label):
    pass

def runAsServer(serverIp):
    pass

def runStubbedClient(addr, port, label):
    client = ClientMock.ClientMock(label)
    client.start(addr, port, baseAddr, basePort)

def runStubbedServer():
    server = ServerMock.ServerMock()
    server.start(baseAddr, basePort)

#testing live local simualtion
def runSimulation():
    server = Process(target = runStubbedServer)

    processes = []
    num = 3

    for i in range(1, num):
        processes.append(Process(target = runStubbedClient, args = (baseAddr, basePort + i, "Client " + str(i))))

    server.start()
    for p in processes: p.start()

    sleep(3)
    server.terminate()
    for p in processes: p.terminate()

def runActualSimulations():
    #removes all the files in the output directory
    Writer.clearDir()

    duration = 20000 #ms

    traditionalTen = Sims.traditional(duration, 3)
    # traditionalHundred = Sims.traditional(duration, 6)
    # traditionalThousand = Sims.traditional(duration, 12)
    # Graphs.plotTraditionalAverage([traditionalTen, traditionalHundred, traditionalThousand])
    # traditionalTen, traditionalHundred = None, None

    # s10 = Sims.basicScyfe(duration, 3, 2, 10)
    # s100 = Sims.basicScyfe(duration, 3, 2, 20)
    # s1000 = Sims.basicScyfe(duration, 3, 2, 40)
    # Graphs.plotThrouput([s10, s100, s1000])
    # s10, s100, s1000 = None, None, None

    # s10 = Sims.basicScyfe(duration, 3, 3, 12)
    # s100 = Sims.basicScyfe(duration, 3, 6, 12)
    # s1000 = Sims.basicScyfe(duration, 3, 12, 12)
    # Graphs.plotMulticastThroughput([s10, s100, s1000])
    # s10, s100, s1000 = None, None, None


    # traditionalThousand.comment = "Traditional"
    # s10m3 = Sims.basicScyfe(duration, 3, 3, 6)
    # s20m3 = Sims.basicScyfe(duration, 3, 3, 12)
    # s10m6 = Sims.basicScyfe(duration, 3, 6, 6)
    # s20m6 = Sims.basicScyfe(duration, 3, 6, 12)
    # Graphs.plotLatency([traditionalThousand, s10m3, s20m3, s10m6, s20m6])

#development tests
def runLocalTests():
    Utils.log(fname, 'Starting tests')
    Stable.runTests()


if __name__ == "__main__":
    # runLocalTests()
    #runSimulation()

    runActualSimulations()

    #runAsClient()
    #runAsServer()

    #runStubbedClient(baseAddr, basePort, "Test Client")
    #runStubbedServer()