import random

class SuperProject():
        def __init__(self, name):
                self.name = name
                self.projects = []

ID_MAX = 2**63

STATUS_CODES = {
        0: 'Not started',
        1: 'In progress',
        2: 'Completed'
}

class Project():
        def __init__(self, objective, required = 1):
                self.objective = objective
                self.required = required
                self.progress = 0
                self.id = random.randint(0, ID_MAX)
                self.dependencies = []

        @property
        def status(self):
                if self.progress == 0:
                        return 0
                elif self.progress < self.required:
                        return 1
                else:
                        return 2
