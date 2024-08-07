#!/usr/bin/env python3
"""
authentication module for db
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    class for db authentication
    """

    def create_session(self, user_id=None):
        """
        create session
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session(self, session_id=None):
        """
        user id for session
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        current_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        expiry_time = sessions[0].created_at + time_span
        if expiry_time < current_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """
        destroys session and logout
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
