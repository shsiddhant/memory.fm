from dataclasses import dataclass


@dataclass
class UserContext:
    user_id: int
    tz: str
