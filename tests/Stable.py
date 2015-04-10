import sys

'''
All relevant classes can be instantiated without crashing. 
'''

from ../client import Client

def run():
  print 'Test:Stable-- testing instantiation of all objects'
  client = Client("TestClient")
  client.soundOff()
  print 'Test:Stable-- success'