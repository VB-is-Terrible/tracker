from common import JSONable
import json
import project as Project
from ChangeSet import ChangeSet


class Patch(JSONable):
        def __init__(self, previous: int, current: int):
                self.create = []
                self.change = []
                self.delete = []
                self.previous = previous
                self.current = current
        excludes = set(['previous', 'current'])

        def json(self):
                return super().json(self.excludes)

        def add_create(self, project: Project.Project):
                string = json.dumps(project, cls=Project.ProjectEncoder)
                self.create.append(string)

        def add_change(self, change_set: ChangeSet):
                string = json.dumps(change_set, cls=Project.ProjectEncoder)
                self.change.append(string)
