"""Module memory_fm.exceptions
Define custom exception classes.

classes defined
---------------
ScrobbleError(Exception)
ParseError(ScrobbleError)
SchemaError(ScrobbleError)
"""

class ScrobbleError(Exception):
    pass


class ParseError(ScrobbleError):
    def __init__(self, filename, *error):
        self.filename = filename
        self.error = error
        super().__init__(f"Cannot parse file '{self.filename}': {self.error}")


class SchemaError(ScrobbleError):
    def __init__(self, error, *column):
        self.column = column
        self.error = error
        super().__init__(self.error)
