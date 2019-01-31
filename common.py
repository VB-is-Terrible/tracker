def valid_property(object, property: str):
        if property.startswith('_'):
                return False
        if callable(getattr(object, property)):
                return False
        return True


class JSONable():
        def json(self, excludes = set()):
                result = {}
                class_dir = dir(type(self))
                props = [x for x in dir(self)
                         if valid_property(self, x)
                         and x not in class_dir
                         and x not in excludes]
                for prop in props:
                        result[prop] = self.__getattribute__(prop)
                return result
