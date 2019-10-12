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


class DuplicateIdException(InputException):
        message = 'Field \'{}\' has duplicate id <{}>'

        def __init__(self, invalid_id: int, field):
                super().__init__(self.message.format(field, invalid_id))


class CyclicDependencyException(InputException):
        message = 'Modifing project <{}> would cause a cyclic dependency chain'

        def __init__(self, project_id: int):
                super().__init__(self.message.format(project_id))


class NonEmptyPropertyException(InputException):
        message = 'Field \'{}\' of {} must be left empty by clients'

        def __init__(self, field: str, obj_name: str):
                super().__init__(self.message.format(field, obj_name))
