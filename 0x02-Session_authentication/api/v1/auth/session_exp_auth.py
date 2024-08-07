#!/usr/bin/env python3
"""
add expiration to Session
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    session auth exp class
    """

    def __init__(self):
        """
        constructor
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create session id
        """
        session_id = super().create_session(user_id)
        if session_id is not None:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session(self, session_id=None):
        """
        session id
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_dict']
            if 'created_at' not in session_dict:
                return None
            current_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            expiry_time = session_dict['created_at'] + time_span
            if expiry_time < current_time:
                return None
            return session_dict['user_id']
