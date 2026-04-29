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
    """If username doesn't exist on Last.fm."""

    def __init__(self, username):
        self.username = username
        super().__init__(f"User not found: {self.username}")


class LastfmAPIError(Exception):
    """Exception for when Last.fm API sends error message as response."""

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"{self.code}: {self.msg}")


class UserLoginRequiredError(LastfmAPIError):
    """User login required. Usually when user privates their recent scrobbles"""

    def __init__(self, msg: str):
        super().__init__(code=17, msg=msg)


class APIKeyError(LastfmAPIError):
    """Error related to Last.fm API Key"""

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)


class RateLimitExceededError(LastfmAPIError):
    """Last.fm rate limit exceeded."""

    def __init__(self, msg: str):
        super().__init__(29, msg)
