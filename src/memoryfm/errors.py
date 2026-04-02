class InvalidDataError(Exception):
    pass


class ParseError(InvalidDataError):
    def __init__(self, filename, error):
        self.filename = filename
        self.error = error
        super().__init__(f"Cannot parse file '{self.filename}': {self.error}")


class SchemaError(InvalidDataError):
    def __init__(self, msg, obj):
        self.msg = msg
        self.obj = obj
        super().__init__(self.msg)
