'''
A group of clients
'''

from utils import *

fname = "Group"

class Group:
    MAX_MEMBERS=3;

    #Requires a reference to its parent. Directly accesses other modules on the parent
    #def __init__(self, parent):
    #   self.parent = parent
    #  self.members = []

    #Just takes a list of group members will throw exception if less than MAX_MEMBERS
    def __init__(self,members):
    	if(len(members)!=MAX_MEMBERS):
    		raise ValueError("Must have "+MAX_MEMBERS+" in a group")
    		
    	self.members=members

    # How this object is represented when logged
    def __repr__(self):
        ret =  'This is an unimplemented description.'
        return ret