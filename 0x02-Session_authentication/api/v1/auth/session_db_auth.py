#!/usr/bin/env python3
"""
SessionDBAuth module for storing session data in the database.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for handling session authentication with a database.
    """
    def create_session(self, user_id=None):
        """
        Create and store a new UserSession instance.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the user_id associated with the session_id.
        """
        if session_id is None:
            return None
        sessions = storage.all(UserSession)
        for session in sessions.values():
            if session.session_id == session_id:
                return session.user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the session ID
        from the request cookie.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        sessions = storage.all(UserSession)
        for session in sessions.values():
            if session.session_id == session_id:
                session.delete()
                storage.save()
                return True
        return False
