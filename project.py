from json import JSONEncoder, loads
from common import JSONable


class Status(JSONable):
        STATUS_CODES_MAJOR = {
                0: 'Not started',
                1: 'In progress',
                2: 'Completed',
                -1: 'Unknown status',
        }
        STATUS_CODES_MINOR = {
                0: None,
                1: 'Awaiting dependencies',
        }

        def __init__(self, major, minor = 0):
                self.major = major
                self.minor = minor

        @property
        def major_code(self):
                return self.STATUS_CODES_MAJOR[self.major]

        @property
        def minor_code(self):
                if self.minor != 0:
                        return self.STATUS_CODES_MINOR[self.minor]
                else:
                        return self.major_code

        def __str__(self):
                return '({}, {}): {}'.format(self.major, self.minor, self.minor_code)


MAX_STATUS = 2
PROGRESS_STATUS = 1
CURRENT_ID = None


def get_id():
        global CURRENT_ID
        temp = CURRENT_ID
        CURRENT_ID += 1
        return temp


class Project(JSONable):
        def __init__(self, system, name, required = 2, id = None,
                     meta = 0, counter = False):
                self.name = name
                self.required = required
                self.progress = 0
                self.system = system
                if id is None:
                        self.id = get_id()
                else:
                        self.id = id
                self.dependencies = []
                self.meta = meta
                self.desc = ''
                self.successors = []
                self.counter = counter

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
                result['status'] = self.status
                return result

        @classmethod
        def fromJSON(cls, json, system):
                obj = loads(json)
                return cls.fromJSONObj(obj, system)

        @classmethod
        def fromJSONObj(cls, obj, system):
                name, required, = obj['name'], obj['required']
                meta = obj['meta']
                counter = obj['counter']
                result = cls(system, name, required, meta = meta,
                             counter = counter)
                result.progress = obj['progress']
                result.dependencies = obj['dependencies']
                result.desc = obj['desc']
                return result


class ProjectEncoder(JSONEncoder):
        def default(self, o):
                try:
                        return o.json()
                except AttributeError:
                        super().default(o)
