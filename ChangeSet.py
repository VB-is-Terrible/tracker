from json import loads
from common import JSONable
from ProjectError import InvalidIdException


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

        BASIC_PROPS = ['name', 'desc', 'required',
                       'progress', 'meta', 'counter']
        ARRAY_PROPS = ['dependencies_add', 'dependencies_remove']

        def json(self):
                result = {}
                result['id'] = self.id
                for prop in self.BASIC_PROPS:
                        value = self.__getattribute__(prop)
                        if value is not None:
                                result[prop] = value
                for prop in self.ARRAY_PROPS:
                        value = self.__getattribute__(prop)
                        if len(value) != 0:
                                result[prop] = value
                return result

        @classmethod
        def fromJSON(cls, json):
                obj = loads(json)
                return cls.fromJSONObj(obj)

        @classmethod
        def fromJSONObj(cls, obj):
                id = obj.get('id', None)
                if id is None:
                        raise InvalidIdException()
                result = cls(id)
                for prop in cls.BASIC_PROPS:
                        if prop in obj:
                                result.__setattr__(prop, obj[prop])
                for prop in cls.ARRAY_PROPS:
                        if prop in obj:
                                result.__setattr__(prop, obj[prop])
                return result

        FIRST_COLUMN = len('dependencies_remove')

        def _col(self, prop: str):
                prop_value = self.__getattribute__(prop)
                return prop.ljust(self.FIRST_COLUMN) + \
                        ': ' + str(prop_value) + '\n'

        def __repr__(self):
                result = self._col('id')
                for prop in self.BASIC_PROPS:
                        result += self._col(prop)
                for prop in self.ARRAY_PROPS:
                        result += self._col(prop)
                return result
