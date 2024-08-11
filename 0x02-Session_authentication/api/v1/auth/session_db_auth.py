#!/usr/bin/env python3
"""
SessionExpAuth module for managing session expiration.
"""

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for managing session expiration.
    """

    def __init__(self):
        """
        Initialize the session duration from an environment variable.
        """
        session_duration = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a new session with an expiration date.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the user_id if the session_id exists and is not expired.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None
        if self.session_duration <= 0:
            return session_data.get("user_id")
        created_at = session_data.get("created_at")
        if created_at is None:
            return None
        if (datetime.now() - created_at).seconds > self.session_duration:
            return None
        return session_data.get("user_id")

    def destroy_session(self, request=None):
        """
        Destroy the session for a user.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True
        return False
