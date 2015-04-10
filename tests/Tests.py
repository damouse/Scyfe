'''
Wrappers simulating a live system for testing the library. 

These wrappers should instantiate and initialize a server and a set of clients, connecting them as 
appropriate, and begin running a set coordinated set of inputs, collecting data on the
performance of the system as appropriate.

'''

import clientcore
from tests import *

# from tests import stable as Stable
from utils import utils

fname = "Tests"


if __name__ == "__main__":
    utils.log(fname, 'Starting all tests')

    stable.runTests()
    # Stable.runTests()

    utils.log(fname, 'All Tests Completed')