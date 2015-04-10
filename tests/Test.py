'''
Wrappers simulating a live system for testing the library. 

These wrappers should instantiate and initialize a server and a set of clients, connecting them as 
appropriate, and begin running a set coordinated set of inputs, collecting data on the
performance of the system as appropriate.

'''

import Stable

if __name__ == "__main__":
  print 'Test Suite-- starting all tests'

  Stable.run()

  print 'Test Suite-- ending all tests'