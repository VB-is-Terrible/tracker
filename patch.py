from common import JSONable
import json
import project


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

        def add_create(self, project: project.Project):
                string = json.dumps(project, cls=project.ProjectEncoder)
                self.create.append(string)
