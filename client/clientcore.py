import sys

'''
Entry point for client-side module. 
'''

class Client:
  def __init__(self, label):
    self.label = label

  def soundOff(self):
    print 'Client named: ' + self.label


if __name__ == "__main__":
  client = Client('Test')
  client.soundOff()