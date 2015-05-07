import matplotlib.pyplot as plot
import os

outputDir = os.getcwd() + "/results/"

def graph(peers, links, groups, tasks, duration):
    test(peers)

def test(peers):
    for peer in peers:
        plot.plot(peer.throughput)

    plot.ylabel('Throuput (bytes)')
    plot.savefig(outputDir + 'test.png')
    # plot.show()
