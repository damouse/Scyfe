

'''
Utility methods.
'''

#platform independant logging function-- can be used to route logs to 
#a central location if need be
def log(name, contents):
    print name + ':: ' + contents