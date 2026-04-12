from __future__ import annotations
import memoryfm.services.user_service as userv
import memoryfm.services.stats_service as stserv


def get_user_service():
    return userv


def get_stats_service():
    return stserv
