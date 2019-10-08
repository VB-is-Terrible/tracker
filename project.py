from json import JSONEncoder, loads
from common import JSONable, check_duplicate_id
from ProjectError import InvalidIdException, InvalidTypeException, \
                         MissingFieldException, InvalidProgressException, \
                         DuplicateIdException


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
                return '({}, {}): {}'.format(self.major,
                                             self.minor,
                                             self.minor_code)

        def __eq__(self, o):
                if self.major == o.major and self.minor == o.minor:
                        return True
                else:
                        return False


MAX_STATUS = 2
PROGRESS_STATUS = 1
CURRENT_ID = None

PROPS = ['name', 'desc', 'required', 'progress', 'meta', 'counter',
         'dependencies']
TYPES = {
        'id': int,
        'name': str,
        'desc': str,
        'required': int,
        'progress': int,
        'meta': int,
        'counter': bool,
        'dependencies': list
}


def get_id():
        global CURRENT_ID
        temp = CURRENT_ID
        CURRENT_ID += 1
        return temp


class Project(JSONable):
        def __init__(self, system, name, required = MAX_STATUS, id = None,
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
                self._status = Status(0, 0)

        @property
        def status(self):
                return self._status

        def update_status(self):
                '''Recalculate the current status, returns whether the status changed'''
                old_status = self._status
                self._status = self._recalculate_status()
                if self._status != old_status:
                        return True
                else:
                        return False

        def _recalculate_status(self):
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
        includes = set(['status'])

        def json(self):
                result = super().json(self.excludes, self.includes)
                result['type'] = 'Project'
                result['status'] = self.status
                return result

        @classmethod
        def fromJSON(cls, json, system):
                obj = loads(json)
                return cls.fromJSONObj(obj, system)

        @classmethod
        def fromJSONObj(cls, obj, system):
                cls._validate_obj(obj, system)
                name, required, = obj['name'], obj['required']
                meta = obj['meta']
                counter = obj['counter']
                result = cls(system, name, required, meta = meta,
                             counter = counter)
                result.progress = obj['progress']
                result.dependencies = obj['dependencies']
                result.desc = obj['desc']
                result.update_status()
                return result

        @classmethod
        def _validate_obj(cls, obj, system):
                for prop in PROPS:
                        if prop not in obj:
                                raise MissingFieldException(prop, 'Project')
                for prop in PROPS:
                        if type(obj[prop]) is not TYPES[prop]:
                                raise InvalidTypeException(
                                        type(obj[prop]),
                                        prop,
                                        'Project',
                                        TYPES[prop])
                for id in obj['dependencies']:
                        if type(id) is not int:
                                raise InvalidTypeException(
                                        type(id),
                                        'id',
                                        'Project.dependencies',
                                        int)
                if obj['required'] < 1:
                        raise InvalidProgressException(obj['required'],
                                                       'required')
                if obj['required'] < obj['progress']:
                        raise InvalidProgressException(obj['progress'],
                                                       'progress')
                if not obj['counter'] and obj['required'] != 2:
                        raise InvalidProgressException(obj['required'],
                                                       'required')

                if obj['progress'] < 0:
                        raise InvalidProgressException(obj['required'],
                                                       'progress')

                for id in obj['dependencies']:
                        if id not in system.projects:
                                raise InvalidIdException(id)

                duplicate = check_duplicate_id(obj['dependencies'])
                if duplicate:
                        raise DuplicateIdException(id, 'dependencies')

        def add_dependency(self, id: int):
                if id in self.dependencies:
                        raise DuplicateIdException(id, 'project.dependencies')
                if id not in self.system.projects:
                        raise InvalidIdException(id)
                self.dependencies.append(id)
                parent = self.system.get_event_by_id(id)
                parent.successors.append(id)

        def remove_dependency(self, id: int):
                if id not in self.dependencies:
                        raise InvalidIdException(id)
                self.dependencies.remove(id)
                parent = self.system.get_event_by_id(id)
                parent.successors.remove(id)


class ProjectEncoder(JSONEncoder):
        def default(self, o):
                try:
                        return o.json()
                except AttributeError:
                        super().default(o)
