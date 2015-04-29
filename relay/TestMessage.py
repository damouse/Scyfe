
# A dummy message used to test message handoffs
class TestMessage:
    def __init__(self, num):
        self.values = []

        for i in range(0, num):
            self.values.append(i)

    def __repr__(self):
        return "I am a TestMessage packet with " + str(len(self.values)) + " sequential integers"

class LabeledPing: 
    def __init__(self, name):
        self.recipient = ""
        self.sender = name

    def __repr__(self):
        return "Messag: labeledPing from " + self.sender + " to " + self.recipient