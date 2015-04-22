
# A dummy message used to test message handoffs
class TestMessage:
    def __init__(self, num):
        self.values = []

        for i in range(0, num):
            self.values.append(i)

    def __repr__(self):
        return "" + str(self.values)