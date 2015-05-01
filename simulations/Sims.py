'''
Simulations. Because protoyping is for squares. 
'''

from utils import Utils
import random

name = "Simulations"

class Peer:
    def __init__(self, label):
        self.name = label
        self.variables = []

        #each element is throughput in that 50ms tick
        self.throughput = []

class Group:
    def __init__(self, label):
        self.peers = []
        self.name = label

class Link:
    def __init__(self, latency, start, end):
        self.start = start
        self.end = end
        self.latency = latency

        #each element is throughput in that 50ms tick
        self.throughput = []

#represents an operation that runs a duration
class Task:
    def __init__(self, name, source):
        self.varname = name
        self.source = source

        self.time = 0

class Variable:
    def __init__(self, name, freq):
        self.name = name
        self.freq = freq #hertz


''' Building Boring Stuff '''
def buildVariables():
    health = Variable("health", 1)
    position = Variable("position", 5)
    money = Variable("money", .1)

    return [health, position, money]


''' Tests '''
def traditional():
    Utils.log(name, "Starting Client-Server Tests")

    peers, links, groups, tasks = [], [], [], []
    sever = Peer("Server")

    for i in range(0, 3): 
        peer = Peer("Peer " + str(i))
        peer.variables = buildVariables()
        links.append(Link(200, peer, server))
        peers.append(peer)

    tasks = run(peers, links, groups)
    log(peers, links, groups, tasks)


''' Main Run '''
def run(peers, links, groups):
    duration = 600 # ms
    step = 100 # ms step
    time = 0
    tasks = []

    while time < duration:

        time += step

    return tasks

def roll(peer, variable):
    roll = random.randrange(0, 1000, 1)

    if roll < variable.freq * 100:
        return 

def log(peers, links, groups, tasks):
    pass





