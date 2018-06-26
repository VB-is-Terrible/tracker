import json

class JSONable():
        def json(self, excludes = set()):
                result = {}
                class_dir = dir(type(self))
                props = [x for x in dir(self) if
                         not x.startswith('_') and
                         not callable(getattr(self, x)) and
                         x not in class_dir and
                         x not in excludes]
                for prop in props:
                        result[prop] = self.__getattribute__(prop)
                return result
