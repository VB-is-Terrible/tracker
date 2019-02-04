from common import JSONable


class Patch(JSONable):
        def __init__(self, previous: int, current: int):
                self.create = []
                self.update = []
                self.delete = []
                self.previous = previous
                self.current = current
        excludes = set(['previous', 'current'])

        def json(self):
                return super().json(self.excludes)
