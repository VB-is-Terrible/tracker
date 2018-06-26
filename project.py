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

class Project(JSONable):
        def __init__(self, system, name, required = 2, id = None):
                self.name = name
                self.required = required
                self.progress = 0
                self.system = system
                if id == None:
                        self.id = get_id()
                else:
                        self.id = id
                self.dependencies = []
                self.meta = 0
                self.desc = ''

        @property
        def status(self):
                if self.meta == 0:
                        if self.progress == 0:
                                depend_status = self._check_depends()
                                if depend_status.major != MAX_STATUS:
                                        return Status(0, 1)
                                else:
                                        return Status(0, 0)
                        elif self.progress < self.required:
                                return Status(PROGRESS_STATUS, 0)
                        else:
                                return Status(MAX_STATUS, 0)
                elif self.meta == 1:
                        return self._check_depends()
                else:
                        return -1

        def _check_depends(self):
                progress = 0
                completed = True
                for depend in self.dependencies:
                        project = self.system.get_event_by_id(depend)
                        if project.status.major != MAX_STATUS:
                                completed = False
                        progress = max(progress, project.status.major)
                if completed:
                        return Status(MAX_STATUS)
                elif progress > 0:
                        return Status(PROGRESS_STATUS)
                else:
                        return Status(0)

        excludes = set(['system'])

        def json(self):
                result = super().json(self.excludes)
                result['type'] = 'Project'
                return result

class ProjectEncoder(JSONEncoder):
        def default(self, o):
                try:
                        return o.json()
                except AttributeError:
                        super().default(o)
