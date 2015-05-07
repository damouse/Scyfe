'''
Simulations. Because protoyping is for squares.

TODO:
    -Peers should gen their own tasks
    -Peers have to receive tasks
    -Task type has to be set when creating tasks 
'''

from utils import Utils

from simulations import Graphs
from simulations import SimModels as Model
import random
import os

name = "Simulations"
outputDir = os.getcwd() + "/results/"

TASK_INPUT = 0 #input to a group triggering a variable change
TASK_UPDATE = 1 #propogation update, that is
TASK_VALIDATION = 2 #not needed?
TASK_HASH = 3 #inter-group hashing


''' Building Boring Stuff '''
def buildVariables():
    health = Model.Variable("health", 1)
    position = Model.Variable("position", 5)
    money = Model.Variable("money", .1)

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
        return Model.Task(variable, peer, target, TASK_UPDATE)

    return None

''' File Utils '''

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

def log(peers, links, groups, tasks, duration):
    clearDir()

    writeSummary("traditional-summary", peers, links, groups, tasks, duration)


''' Tests '''
def traditional(duration):
    Utils.log(name, "Starting Client-Server Tests...")
    peers, links, groups, tasks = [], [], [], []
    server = Model.Peer("Server")
    peers.append(server)

    for i in range(0, 3): 
        peer = Model.Peer("Peer " + str(i))
        peer.variables = buildVariables()
        links.append(Model.Link(200, peer, server))
        peers.append(peer)

    tasks = run(peers, links, groups, duration)
    log(peers, links, groups, tasks, duration)
    Graphs.graph(peers, links, groups, tasks, duration)

    Utils.log(name, "done")


''' Random Testing '''
def test():
    pass


