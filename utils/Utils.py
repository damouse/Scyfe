'''
Utility methods.
'''

DEBUG_LOG = True

#platform independant logging function-- can be used to route logs to 
#a central location if need be
def log(name, contents):
    print name + ':\t ' + contents


#debug logging
def dlog(name, contents):
    if DEBUG_LOG:
        print name + ':\t ' + contents