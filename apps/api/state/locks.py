from __future__ import annotations
import asyncio

user_locks: dict[str, asyncio.Lock] = {}


def get_lock(username: str):
    if username not in user_locks:
        user_locks[username] = asyncio.Lock()
    return user_locks[username]
