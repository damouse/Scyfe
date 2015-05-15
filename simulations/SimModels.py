'''
Model objects used and passed around by the main loop
'''

import random

TASK_INPUT = 0 #input to a group triggering a variable change
TASK_UPDATE = 1 #propogation update, that is
TASK_GROUP_PROP = 2
TASK_HASH = 3 #inter-group hashing

startingTaskId = 0

class Variable:
    def __init__(self, name, freq):
        self.name = name
        self.freq = freq #hertz

class Peer:
    def __init__(self, label):
        self.name = label
        self.variables = buildVariables()
        self.server = False

        #each element is throughput in that 50ms tick
        self.throughput = []
        self.next = []

        self.group = None
        self.areaOfInterest = []
        self.latency = 0

    #receive an incoming task and decide what to do with it
    def receiveTask(self, task):
        if task.type == TASK_HASH:
            ret = []
            for peer in self.areaOfInterest:
                ret.append(Task(task.variable, self, peer, TASK_UPDATE))
            #wait until all the hashes come in first and then broadcast the new updates to subs
            return ret

        if task.type == TASK_UPDATE:
            ret = []
            for peer in self.group.peers:
                ret.append(Task(task.variable, self, peer, TASK_GROUP_PROP))
            return ret
        
        return []

    def __eq__(self, other):
        if not isinstance(other, Peer): return False
        return self.name == other.name

    def __repr__(self):
        return self.name 

    def write(self):
        return self.name + "\n\tLinks: " + str(self.next) + "\n\tThroughput Signals: " + str(self.throughput) 


def buildVariables():
    health = Variable("health", 1)
    position = Variable("position", 5)
    money = Variable("money", .1)

    return [health, position, money]


class Group:
    def __init__(self, label):
        self.peers = []
        self.name = label

    def addPeer(self, peer):
        self.peers.append(peer)
        peer.group = self

    def __repr__(self):
        return self.name + " " + str(self.peers)

    #makes links between all the peers in the group. Returns a set of links
    def link(self):
        links = []
        for i in range(0, len(self.peers)):
            for j in range(i + 1, len(self.peers)):
                links.append(Link(200, self.peers[i], self.peers[j]))

        return links

    #link this group with another group given one peer in the group
    def linkGroup(self, group):
        #pick the peer with the least number of existing links to link up 
        shortestSelf = shortestNext(self.peers)
        shortestRemote = shortestNext(group.peers)

        shortestSelf.areaOfInterest.append(shortestRemote)
        shortestRemote.areaOfInterest.append(shortestSelf)

        return Link(200, shortestSelf, shortestRemote)


def shortestNext(peers):
    shortest = 12345678
    target = peers[0]
    for peer in peers:
        if len(peer.next) < shortest: 
            shortest = len(peer.next)
            target = peer

    return target

class Link:
    def __init__(self, latency, start, end):
        self.next = [start, end]
        self.name = "[" + self.next[0].name + "]-[" + self.next[1].name + "]"
        self.latency = latency

        start.next.append(self)
        end.next.append(self)

        #each element is throughput in that 50ms tick
        self.throughput = []

    def __eq__(self, other):
        if not isinstance(other, Link): return False
        return self.name == other.name

    def __repr__(self):
        return self.name + " (" + str(self.latency) + "ms)" 

    def write(self):
        return self.__repr__() + "\n\t" + str(self.throughput) 

#represents an operation that runs a duration
class Task:
    def __init__(self, var, source, target, taskType):
        global startingTaskId
        self.taskId = startingTaskId
        startingTaskId += 1

        self.variable = var
        self.type = taskType

        self.source = source
        self.target = target

        if self.type == TASK_HASH: self.size = 1024
        else: self.size = random.randrange(0, 4096, 1024)

        self.startTime = 0
        self.time = 0
        self.currentTimeDown = 0 #the amount of time left on 

        self.route = None
        self.position = source

    def __repr__(self):
        ret = "#" + str(self.taskId) + ": " + self.variable.name + " " + str(self.size) + " bytes time: " + str(self.time) + "ms \n\t"
        route = ""

        for item in self.routeHistory: route += str(item) + " - "
        ret += route
        return ret 

    def setRoute(self, route):
        self.route = route
        self.routeHistory = list(route)