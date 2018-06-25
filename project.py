import random
from json import JSONEncoder
from common import JSONable

STATUS_CODES = {
        0: 'Not started',
        1: 'In progress',
        2: 'Completed'
}

CURRENT_ID = None

def get_id():
        global CURRENT_ID
        temp = CURRENT_ID
        CURRENT_ID += 1
        return temp

class SuperProject(JSONable):
        def __init__(self, name):
                self.name = name
                self.projects = []
                self.id = get_id()

class Project(JSONable):
        def __init__(self, objective, required = 2):
                self.objective = objective
                self.required = required
                self.progress = 0
                self.id = get_id()
                self.dependencies = []

        @property
        def status(self):
                if self.progress == 0:
                        return 0
                elif self.progress < self.required:
                        return 1
                else:
                        return 2

class ProjectEncoder(JSONEncoder):
        def default(self, o):
                try:
                        return o.json()
                except AttributeError:
                        super().default(o)
