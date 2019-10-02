from json import loads
from common import JSONable
from ProjectError import InvalidIdException, MissingFieldException, \
                         InvalidTypeException, InvalidProgressException


BASIC_PROPS = ['name', 'desc', 'required',
               'progress', 'meta', 'counter']
ARRAY_PROPS = ['dependencies_add', 'dependencies_remove']
TYPES = {
        'id': int,
        'name': str,
        'desc': str,
        'required': int,
        'progress': int,
        'meta': int,
        'counter': bool,
        'dependencies_add': list,
        'dependencies_remove': list,
}


class ChangeSet(JSONable):
        def __init__(self, id: int):
                self.id = id
                self.name = None
                self.desc = None
                self.required = None
                self.progress = None
                self.dependencies_add = []
                self.dependencies_remove = []
                self.meta = None
                self.status = None
                self.counter = None

        def json(self):
                result = {}
                result['id'] = self.id
                for prop in BASIC_PROPS:
                        value = self.__getattribute__(prop)
                        if value is not None:
                                result[prop] = value
                for prop in ARRAY_PROPS:
                        value = self.__getattribute__(prop)
                        if len(value) != 0:
                                result[prop] = value
                return result

        @classmethod
        def fromJSON(cls, json, system):
                obj = loads(json)
                return cls.fromJSONObj(obj, system)

        @classmethod
        def fromJSONObj(cls, obj, system):
                cls._validate_obj(obj, system)
                id = obj.get('id', None)
                if id is None:
                        raise InvalidIdException()
                result = cls(id)
                for prop in BASIC_PROPS:
                        if prop in obj:
                                result.__setattr__(prop, obj[prop])
                for prop in ARRAY_PROPS:
                        if prop in obj:
                                result.__setattr__(prop, obj[prop])
                return result

        FIRST_COLUMN = len('dependencies_remove')

        def _col(self, prop: str):
                prop_value = self.__getattribute__(prop)
                return (prop.ljust(self.FIRST_COLUMN)
                        + ': ' + str(prop_value) + '\n')

        def __repr__(self):
                result = self._col('id')
                for prop in BASIC_PROPS:
                        result += self._col(prop)
                for prop in ARRAY_PROPS:
                        result += self._col(prop)
                return result

        @staticmethod
        def _validate_obj(obj, system):
                if 'id' not in obj:
                        raise MissingFieldException('id', 'ChangeSet')
                if type(obj['id']) is not int:
                        raise InvalidTypeException('id', 'ChangeSet', int)
                if obj['id'] not in system.projects:
                        raise InvalidIdException(obj['id'])
                for prop in BASIC_PROPS + ARRAY_PROPS:
                        if prop not in obj:
                                continue
                        if type(obj[prop]) is not TYPES[prop]:
                                raise InvalidTypeException(
                                        type(obj[prop]),
                                        prop,
                                        'ChangeSet',
                                        TYPES[prop]
                                )
                for prop in ARRAY_PROPS:
                        if prop not in obj:
                                continue
                        for id in obj[prop]:
                                if type(id) is not int:
                                        raise InvalidTypeException(
                                                type(id),
                                                'id',
                                                'ChangeSet.' + prop,
                                                TYPES[prop]
                                        )
                                if id not in system.projects:
                                        raise InvalidIdException(id)

                if 'required' in obj:
                        if obj['required'] < 1:
                                raise InvalidProgressException(
                                        'required', 'ChangeSet')
                        if 'counter' in obj and obj['counter'] is False:
                                if obj['required'] != 2:
                                        raise InvalidProgressException(
                                                'required', 'ChangeSet')
                        if 'progress' in obj:
                                if obj['progress'] > obj['required']:
                                        raise InvalidProgressException(
                                                'progress', 'ChangeSet')

                if 'progress' in obj:
                        if obj['progress'] < 0:
                                raise InvalidProgressException(
                                        obj['progress'], 'ChangeSet.progress')
        @staticmethod
        def validate_with_project(change_set, project):
                if change_set.required is not None and \
                   change_set.progress is None:
                        if project.progress > change_set.required:
                                raise InvalidProgressException(
                                        'required', 'ChangeSet')
                if change_set.counter is False and \
                   change_set.required is None:
                        if project.required != 2:
                                raise InvalidProgressException(
                                        'counter', 'ChangeSet')
                if change_set.required is None and \
                   change_set.progress is not None:
                        if project.required < change_set.progress:
                                raise InvalidProgressException(
                                        'progress', 'ChangeSet')

                pass
