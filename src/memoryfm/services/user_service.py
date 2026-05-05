from __future__ import annotations
import json
from typing import TYPE_CHECKING
import logging
from pydantic import ValidationError
import requests
from sqlalchemy.exc import SQLAlchemyError
import memoryfm.storage.user_repo as urepo
from memoryfm.util.datetime_util import validate_tz
from memoryfm.errors import (
    APIKeyError,
    InvalidDataError,
    LastfmAPIError,
    RateLimitExceededError,
    UserNotFoundError,
)
from memoryfm.models.service_helpers import UserContext, parse_lastfm_api_user_info
from memoryfm.models.sync_status import UserExist

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from memoryfm.models.sync_status import EnsureUserStatus


logger = logging.getLogger(__name__)


def create_user(
    session: Session,
    username: str,
    tz: str | None = "Etc/UTC",
    overwrite: bool = False,
):
    tz = validate_tz(tz)
    try:
        user = urepo.get_user_by_username(session, username)
        if overwrite and user:
            urepo.delete_user(session, user.id)
        if not user:
            urepo.insert_user(session, username, tz)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    except Exception:
        raise


def delete_user(session: Session, user_id: int):
    try:
        urepo.delete_user(session, user_id)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise


def get_user_context(session: Session, username: str) -> UserContext:
    user = urepo.get_user_by_username(session, username)
    if user:
        return UserContext(user.id, user.tz)
    else:
        raise UserNotFoundError(username)


def lastfm_get_user_info(
    username: str,
    api_key: str,
):
    """
    Fetch user info from last.fm API method user.getInfo
    Parameters
    ----------
    username : str
        A last.fm username.
    api_key : str
        A valid last.fm API key

    """
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={api_key}&format=json"
    response = requests.get(url)
    try:
        response_data = response.json()
        return parse_lastfm_api_user_info(response_data)
    except json.JSONDecodeError:
        raise
    except InvalidDataError:
        raise
    except ValidationError:
        raise


def ensure_user(
    session: Session, username: str, api_key: str, ensure_user_status: EnsureUserStatus
):
    ensure_user_status.status = UserExist.Checking
    ensure_user_status.retry = 1
    ensure_user_status.total_retries = 5
    while True:
        try:
            userinfo = lastfm_get_user_info(username, api_key)
            create_user(session, username)
            ensure_user_status.status = UserExist.Exists
            return userinfo
        except LastfmAPIError as e:
            ensure_user_status.status = UserExist.Error
            if (
                e.code in (8, 11)
                and ensure_user_status.retry <= ensure_user_status.total_retries
            ):
                ensure_user_status.retry += 1
                continue
            elif e.code == 6:
                raise UserNotFoundError(username)
            elif e.code in (10, 26):
                raise APIKeyError(e.code, e.msg)
            elif e.code == 29:
                raise RateLimitExceededError(e.msg)
        except Exception as e:
            ensure_user_status.status = UserExist.Error
            raise UserNotFoundError(username, *e.args)
