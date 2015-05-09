''' 
File utils. Clear the output directory and write out provided information as needed.
'''

import os
outputDir = os.getcwd() + "/results/"


''' Public Interface '''
def log(peers, links, groups, tasks, duration):
    writeSummary("traditional-summary", peers, links, groups, tasks, duration)



''' Printing calls- reusable by multiple tests '''
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


''' Internal Helpers'''
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
