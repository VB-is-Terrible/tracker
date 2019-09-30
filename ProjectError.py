class InputException(Exception):
        pass


class InvalidIdException(InputException):
        message = 'Invalid id: <{}>'

        def __init__(self, id: int):
                super().__init__(self.message.format(id))


class InvalidTypeException(InputException):
        message = 'Invalid type {} for field \'{}\' in {}, expected {}'

        def __init__(self, bad_type, missing_field: str, dict_name: str,
                     expected):
                super().__init__(self.message.format(bad_type, missing_field,
                                                     dict_name, expected))


class MissingFieldException(InputException):
        message = 'Could not find field: <{}> in \'{}\''

        def __init__(self, missing_field: str, dict_name: str):
                super().__init__(self.message.format(missing_field, dict_name))


class InvalidProgressException(InputException):
        message = 'Field \'{}\' has invalid value <{}>'

        def __init__(self, invalid_value, field):
                super().__init__(self.message.format(field, invalid_value))
