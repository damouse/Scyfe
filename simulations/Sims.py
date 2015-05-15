'''
Simulations. Because protoyping is for squares.

This file contains the core run loop for the simulation model as well as the test setup functions. 

Model objects are found in SimModels.py. 
Graphs.py holds graph output code
Writer.py produces output files in the results folder (if applicable)

Each class and method should be reasonably well documented. 

TODO:
    -Peers should generate their own tasks
    -Peers have to receive tasks and do something interesting with them
    -Build the actual tests!
'''

from utils import Utils

from simulations import Graphs
from simulations import SimModels as Model
from simulations import Writer
from simulations import timer
import random
import os
import pprint

TRADITIONAL = False
VERBOSE_TIMER = True

#memoization of routes between all peers in the graph
routeMemoization = {}

''' Main Funcitons '''
# The main run loop for the simulation. "Ticks" in constant millisecond increments
# advancing tasks along their routes until the target time is reached (duration.)
#
# Begins with the set of all peers, links, and groups. Each tick, each peer is asked 
# for new input tasks (or packets). After, each task is propogated through the network 
# in a somewhat time-realistic way. 
def run(peers, links, groups, duration):
    step = 100 # ms step
    time = 0

    global routeMemoization
    routeMemoization = {}

    liveTasks, deadTasks = [], []

    while time < duration:
        time += step
        print "Starting tick: " + str(time)

        # the throughput per tick is measured in an array. Each tick, append a 
        # 0 to the array to signify the start of this periods throughput. All tasks 
        # that traverse peers or links during this time will increment the last element
        # of that array. 
        for link in links: link.throughput.append(0)
        for peer in peers: peer.throughput.append(0)

        #generate new tasks
        for peer in peers:
            for var in peer.variables:
                for task in generateVariable(peer, peers, var):
                    route = buildRoute(task, task.source)
                    task.setRoute(route)
                    task.startTime = time
                    liveTasks.append(task)
                    # pprint.pprint(routeMemoization)


        #tick existing tasks
        for task in liveTasks:
            if advanceTask(task, step): 
                liveTasks.remove(task)
                deadTasks.append(task)

                #deliver the task to the target. They will return any new tasks.
                newTasks = task.target.receiveTask(task)
                for task in newTasks: 
                    task.setRoute(buildRoute(task, task.source))
                    task.startTime = time
                liveTasks.extend(newTasks)

    #return the list of tasks that completed their journey
    return deadTasks

# Given a peer, the set of all peers, and a variable, "roll" the variable and 
# return a Task object or None. 
#
# Each variable is tested against a random number by its field 'freq'.
#
# The returned task represents an input at that given peer. The protocol
# takes over from there
def generateVariable(peer, peers, variable):
    roll = random.randrange(0, 1000, 1)
    ret = []

    if roll < variable.freq * 100:
        #if we are running traditional server tests then the server is the only recipient of any update
        if TRADITIONAL:
            return [Model.Task(variable, peer, [x for x in peers if x.server][0], Model.TASK_HASH)]

        for neighbor in peer.group.peers:
            if neighbor == peer: continue
            ret.append(Model.Task(variable, peer, neighbor, Model.TASK_HASH))

    return ret

# Move forward by the given amount of time. Return true if the task is finished
#
# If the task is currently at a peer, move the task onto the next link in its route.
# If that task is on a link, check and see if the link latency has completed and push 
# the task through when this is the case. 
def advanceTask(task, advance):
    if task.position == task.target: return True

    task.currentTimeDown -= advance
    task.time += advance

    if task.currentTimeDown <= 0:
        task.position = task.route[0]
        task.route.pop(0)
        task.currentTimeDown = task.position.latency

        task.position.throughput[-1] += task.size

    return False

# Recursive- builds a list of peers and links for a Task on the path to its target. 
#
# Given a task and the current node, recall the function recursively on the node's 
# children until the target node is reached. Return the shortest path. 
earlyStop = False
def buildRoute(task, start, oldPath=[]):
    # Copy the path and add this peer to the list
    path = list(oldPath)
    path.extend([start])

    #found the target node. Return the path so far
    if start == task.target:
        return path

    if start.name in routeMemoization:
        if task.target.name in routeMemoization[start.name]:
            return list(routeMemoization[start.name][task.target.name])
    else:
        routeMemoization[start.name] = {}

    shortest = None

    # Recursively call this method on children of current node, checking 
    # the length of the returned paths. Return the shortest, or None if the 
    # target node could not be found. 
    for child in start.next:
        if child not in path:
            shortest = buildRoute(task, child, path)

            if shortest: break
            
            newpath = buildRoute(task, child, path)

            if newpath: 
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath

    if shortest: routeMemoization[start.name][task.target.name] = list(shortest)
    return shortest


''' Tests '''
# A traditional client-server architecture. Validation and propoogation currently happens
# the same way it should in Scyfe, but server should batch updates and not 
# reply to each client individually. 
def traditional(duration, numClients = 3):
    print "Starting Client-Server Tests..."

    #switch on the global
    global TRADITIONAL
    TRADITIONAL = True

    peers, links, groups, tasks = [], [], [], []

    server = Model.Peer("Server")
    server.server = True
    peers.append(server)

    group = Model.Group("Group 1")
    group.addPeer(server)
    groups.append(group)

    for i in range(0, numClients): 
        peer = Model.Peer("Peer " + str(i))
        links.append(Model.Link(200, peer, server))
        peers.append(peer)
        group.addPeer(peer)

    server.areaOfInterest = peers

    tasks = run(peers, links, groups, duration)
    # Writer.log(peers, links, groups, tasks, duration)

    TRADITIONAL = False
    print "done"

    stats = Writer.Stats(peers, links, groups, tasks)
    stats.num = numClients
    stats.duration = duration
    stats.connectivity = 0
    stats.multicast = 0

    return stats


def basicScyfe(duration, groupSize, conectivityFactor, numClients = 10):
    print "Starting Scyfe Tests..."

    peers, links, groups, tasks = [], [], [], []
    numGroups = numClients / groupSize;

    for i in range(0, numGroups):
        group = Model.Group("Group " + str(i))
        groups.append(group)

        for j in range(0, groupSize):
            peer = Model.Peer("Peer " + str(i) + str(j))
            peers.append(peer)
            group.addPeer(peer)

        links += group.link()

    for i in range(0, len(groups)):
        for j in range(1, conectivityFactor + 1):
            links.append(groups[i].linkGroup(groups[j % len(groups)]))


    tasks = run(peers, links, groups, duration)
    # Writer.log(peers, links, groups, tasks, duration)

    print "done"

    stats = Writer.Stats(peers, links, groups, tasks)
    stats.num = numClients
    stats.duration = duration
    stats.connectivity = conectivityFactor
    stats.multicast = conectivityFactor

    return stats

''' Random Testing '''
def test():
    pass


