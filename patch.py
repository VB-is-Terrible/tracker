from common import JSONable

class Patch(JSONable):
        def __init__(self):
                self.create = []
                self.update = []
                self.delete = []
        
