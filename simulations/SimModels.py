startingTaskId = 0

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

        self.route = self.routing(self.source)
        self.routeHistory = list(self.route)

    def __repr__(self):
        ret = "#" + str(self.taskId) + ": " + self.variable.name + " " + str(self.size) + "bytes time: " + str(self.time) + "ms \n\t"
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

            self.position.throughput[-1] += self.size

        return False

class Variable:
    def __init__(self, name, freq):
        self.name = name
        self.freq = freq #hertz
