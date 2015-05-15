import matplotlib.pyplot as plot
import os

outputDir = os.getcwd() + "/results/"

def graph(peers, links, groups, tasks, duration):
    test(peers)

def graphAllPeers(peers):
    for peer in peers:
        plot.plot(peer.throughput)

    plot.ylabel('Throuput (bytes)')
    plot.xlabel('Time (10s of ms)')
    plot.savefig(outputDir + 'peerThroughput.png')

def plotThrouput(stats):
    results = []
    for test in stats:
        sumT = 0
        for i in range(0, len(stats[0].peers[0].throughput)):
            for peer in test.peers:
                sumT += peer.throughput[i]

            test.average.append(sumT / len(test.peers))
            sumT = 0

    for test in stats:
        plot.plot(test.average)

    plot.ylabel('Throuput (bytes)')
    plot.xlabel('Time (100s of ms)')
    plot.savefig(outputDir + 'avg_throughput.png')


def plotTraditionalAverage(stats):
    lines = []

    for test in stats:
        sumClients = 0
        server = [x for x in test.peers if x.server][0]
        peers = [x for x in test.peers if not x.server]

        for i in range(0, len(stats[0].peers[0].throughput)):
            for peer in peers:
                sumClients += peer.throughput[i]

            test.average.append(sumClients / len(test.peers))
            sumClients = 0

        addedPlot, = plot.plot(toKB(test.average), label = "Clients, N=" + str(len(test.peers)))
        lines.append(addedPlot)
        addedPlot, = plot.plot(toKB(server.throughput), label = "Server, N=" + str(len(test.peers)))
        lines.append(addedPlot)

    plot.legend(handles = lines)
    plot.ylabel('Throuput (KB)')
    plot.xlabel('Time (100s of ms)')
    plot.savefig(outputDir + 'avg_throughput.png')

def toKB(values):
    return [x / 1024 for x in values]
