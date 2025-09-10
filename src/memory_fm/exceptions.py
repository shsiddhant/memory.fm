"""Module memory_fm.exceptions
Define custom exception classes.

classes defined
---------------
ScrobbleError(Exception)
EmptyJSONError(ScrobbleError)
SchemaError(ScrobbleError)
"""

class ScrobbleError(Exception):
    pass


class EmptyJSONError(ScrobbleError):
    def __init__(self, filename):
        self.filename = filename 
        super().__init__(f"File '{self.filename}' contains empty JSON data.")


class SchemaError(ScrobbleError):
    def __init__(self, error, column):
        self.column = column
        self.error = error
        super().__init__(self.error)
