import json

class JSONable():
        def json(self):
                result = {}
                props = [x for x in dir(self) if not x.startswith('_') and not callable(getattr(self, x))]
                for prop in props:
                        result[prop] = self.__getattribute__(prop)
                return result
        
