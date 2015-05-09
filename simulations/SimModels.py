'''
Model objects used and passed around by the main loop
'''



startingTaskId = 0

class Variable:
    def __init__(self, name, freq):
        self.name = name
        self.freq = freq #hertz

class Peer:
    def __init__(self, label):
        self.name = label
        self.variables = buildVariables()

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

def buildVariables():
    health = Variable("health", 1)
    position = Variable("position", 5)
    money = Variable("money", .1)

    return [health, position, money]

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
        global startingTaskId
        self.taskId = startingTaskId
        startingTaskId += 1

        self.variable = var
        self.type = taskType

        self.source = source
        self.target = target
        self.size = 1000 #bytes

        self.time = 0
        self.currentTimeDown = 0 #the amount of time left on 

        self.route = None
        self.position = source

    def __repr__(self):
        ret = "#" + str(self.taskId) + ": " + self.variable.name + " " + str(self.size) + "bytes time: " + str(self.time) + "ms \n\t"
        route = ""

        for item in self.routeHistory: route += str(item) + " - "
        ret += route
        return ret 

    def setRoute(self, route):
        self.route = route
        self.routeHistory = list(route)