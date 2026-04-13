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


class UserNotFoundError(Exception):
    def __init__(self, username):
        self.username = username
        super().__init__(f"User not found: {self.username}")


class LastfmAPIError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"{self.code}: {self.msg}")
