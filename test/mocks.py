class MockContainers():
    def __init__(self, container_lst):
        self.containers = container_lst

class MockImage():
    def __init__(self, name):
        self.image = name

class MockLabels():
    def __init__(self, labels):
        self.labels = labels

class MockStartTime():
    def __init__(self, time):
        self.start_time = time