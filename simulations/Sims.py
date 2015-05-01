'''
Simulations. Because protoyping is for squares. 
'''

from utils import Utils
import random
import os

name = "Simulations"

class Peer:
    def __init__(self, label):
        self.name = label
        self.variables = []

        #each element is throughput in that 50ms tick
        self.throughput = []
        self.links = []

    def __eq__(self, other):
        return self.name == other.name

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

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

#represents an operation that runs a duration
class Task:
    def __init__(self, var, source, target):
        self.varname = var.name
        self.source = source
        self.target = target
        self.size = 1000 #bytes

        self.time = 0
        self.currentTimeDown = 0 #the amount of time left on 

        self.route = None
        self.position = source

        self.route = routing(self.source, self.target)

    # find a route by BFSing the links and nodes, return the path
    # assumes a path exists!
    def routing(current, target, seenNodes = []):
        for link in current.links:
            seenLinks = []
            nextPeer = link.start if link.start == current else link.end

            #ignore nodes already seen
            if nextPeer in seenNodes: continue
            seenNodes.append(nextPeer)

            path = [link, nextPeer]

            #found the target node
            if nextPeer == target: return path

            #not a seen node, not the target, call recursively. If the call returns None
            # then nothing was found
            nextPath = routing(nextPeer, target, seenNodes)
            if nextPath is not None: return path.extend(nextPath)

        #fell through the whole list, no more peers, return nothing
        return None

    #move forward by the given amount of time. Return true if the task is finished
    def advance(self, advance):
        if self.position == self.target: return True

        self.currentTimeDown -= advance
        self.time += advance

        if currentTimeDown == 0:
            self.position = self.route[0]
            self.route.pop(0)

            self.position.throughput[-1] += self.size

        return False

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


''' Main Run '''
def run(peers, links, groups, duration):
    step = 100 # ms step
    time = 0

    liveTasks, deadTasks = [], []

    while time < duration:
        time += step
        [x.throughput.append(0) for x in links]

        #generate new tasks
        for peer in peers:
            peer.throughput.append(0)

            for var in peer.variables:
                task = roll(peer, var)

                if task is not None:
                    liveTasks.append(task)

        #tick existing tasks
        for task in liveTasks:

            # the tasks is completed
            if task.advance(step): 
                liveTasks.remove(task)
                deadTasks.append(task)

    return tadeadTaskssks

def roll(peer, peers, variable):
    roll = random.randrange(0, 1000, 1)

    target = peer
    while target == peer: target = random.choice(peers)

    if roll < variable.freq * 100:
        return Task(variable.name, peer, target)

    return None

def log(peers, links, groups, tasks):
    clearDir()


''' File Utils '''
outputDir = os.getcwd() + "/results/"
def clearDir():
    for fname in os.listdir(outputDir):
        file_path = os.path.join(outputDir, fname)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

def makeFile(name):
    name = name + '.txt'
    pathname = outputDir + name

    if not os.path.exists(os.path.dirname(pathname)):
        os.makedirs(os.path.dirname(pathname))

    return open(pathname, "w") 

def writeCase(outFile, contents):
    # see here for CSV printing fun
    #http://stackoverflow.com/questions/18952716/valueerror-i-o-operation-on-closed-file
    outFile.write(contents)
    outFile.close()


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


''' Random Testing '''
def test():
    clearDir()
    outFile = makeFile("test")
    writeCase(outFile, "Hey guisee!")
    





