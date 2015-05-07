'''
Simulations. Because protoyping is for squares.

TODO:
    -Peers should gen their own tasks
    -Peers have to receive tasks
    -Task type has to be set when creating tasks 
'''

from utils import Utils
import random
import os

name = "Simulations"

TASK_INPUT = 0 #input to a group triggering a variable change
TASK_UPDATE = 1 #propogation update, that is
TASK_VALIDATION = 2 #not needed?
TASK_HASH = 3 #inter-group hashing

taskId = 0

class Peer:
    def __init__(self, label):
        self.name = label
        self.variables = []

        #each element is throughput in that 50ms tick
        self.throughput = []
        self.next = []

        # receiving and task generation
        self.outgoing = []

    #receive an incoming task and decide what to do with it
    def receiveTask(self, task):
        pass

    #generate outgoing tasks based on var rolls
    def generateTasks(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, Peer): return False
        return self.name == other.name

    def __repr__(self):
        return self.name 

    def write(self):
        return self.name + "\n\tLinks: " + str(self.next) + "\n\tThroughput Signals: " + str(self.throughput) 

class Group:
    def __init__(self, label):
        self.peers = []
        self.name = label

    def __repr__(self):
        return self.name + " " + str(self.peers)

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
        self.id = taskId
        taskId += 1

        self.variable = var
        self.type = taskType

        self.source = source
        self.target = target
        self.size = 1000 #bytes

        self.time = 0
        self.currentTimeDown = 0 #the amount of time left on 

        self.route = None
        self.position = source

        self.route = self.routing(self.source)
        self.routeHistory = list(self.route)

    def __repr__(self):
        ret = self.variable.name + " " + str(self.size) + "bytes time: " + str(self.time) + "ms \n\t"
        route = ""

        for item in self.routeHistory: route += str(item) + " - "
        ret += route
        return ret 

    def routing(self, start, oldPath=[]):
        #required to avoid references to the list
        path = list(oldPath)
        path.extend([start])
        if start == self.target:
            return path

        shortest = None

        for child in start.next:
            if child not in path:
                newpath = self.routing(child, path)

                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    #move forward by the given amount of time. Return true if the task is finished
    def advance(self, advance):
        if self.position == self.target: return True

        self.currentTimeDown -= advance
        self.time += advance

        if self.currentTimeDown <= 0:
            self.position = self.route[0]
            self.route.pop(0)

            print 'Parent: ' + str(self.position)
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

        for link in links: link.throughput.append(0)
        for peer in peers: peer.throughput.append(0)

        #generate new tasks
        for peer in peers:
            for var in peer.variables:
                task = roll(peer, peers, var)

                if task != None:
                    liveTasks.append(task)

        #tick existing tasks
        for task in liveTasks:

            # the tasks is completed
            if task.advance(step): 
                liveTasks.remove(task)
                deadTasks.append(task)

    return deadTasks

def roll(peer, peers, variable):
    roll = random.randrange(0, 1000, 1)

    target = peer
    while target == peer: target = random.choice(peers)

    if roll < variable.freq * 100:
        return Task(variable, peer, target)

    return None

def log(peers, links, groups, tasks, duration):
    clearDir()

    writeSummary("traditional-summary", peers, links, groups, tasks, duration)


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

# see here for CSV printing fun
#http://stackoverflow.com/questions/18952716/valueerror-i-o-operation-on-closed-file
def writeSummary(name, peers, links, groups, tasks, duration):
    outFile = makeFile(name)
    outFile.write(str(duration / 1000) + " second run\n")

    outFile.write("--Peers--\n")
    for peer in peers: outFile.write(peer.write() + '\n')

    outFile.write("\n--Links--\n")
    for link in links: outFile.write(link.write() + '\n')

    outFile.write("\n--Groups--\n")
    for group in groups: outFile.write(group + '\n')

    outFile.write("\n--Tasks--\n")
    for task in tasks: outFile.write(str(task) + '\n')

    outFile.close()


''' Tests '''
def traditional(duration):
    Utils.log(name, "Starting Client-Server Tests...")
    peers, links, groups, tasks = [], [], [], []
    server = Peer("Server")
    peers.append(server)

    for i in range(0, 3): 
        peer = Peer("Peer " + str(i))
        peer.variables = buildVariables()
        links.append(Link(200, peer, server))
        peers.append(peer)

    tasks = run(peers, links, groups, duration)
    log(peers, links, groups, tasks, duration)

    Utils.log(name, "done")


''' Random Testing '''
def test():
    peers, links, groups, tasks = [], [], [], []
    server = Peer("Server")

    for i in range(0, 3): 
        peer = Peer("Peer " + str(i))
        peer.variables = buildVariables()
        links.append(Link(200, peer, server))
        peers.append(peer)

    var = Variable("TestRoute", 1)
    task = Task(var, peers[0], peers[-1])

    peers.append(server)

    print "Moving from " + peers[0].name + " to " + peers[-1].name

    print "Links"
    for link in links:
        print '\t' + str(link)

    print '\nPeers'
    for peer in peers:
        print '\t' + peer.write()

    print '\nRoute'
    print '\t' + str(task.route)
    
    duration = 1000
    step = 100 # ms step
    time = 0

    liveTasks, deadTasks = [task], []

    while time < duration:
        time += step
        [x.throughput.append(0) for x in links]

        #generate new tasks
        for peer in peers:
            peer.throughput.append(0)

        #tick existing tasks
        for task in liveTasks:

            # the tasks is completed
            if task.advance(step): 
                print 'Task Completed'
                liveTasks.remove(task)
                deadTasks.append(task)

    log(peers, links, groups, tasks, duration)





