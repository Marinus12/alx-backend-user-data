#!/usr/bin/env python3
"""
UserSession model for storing session data in the database.
"""

from models.base import Base
import models
from uuid import uuid4
from datetime import datetime


class UserSession(Base):
    """
    UserSession class to store user_id and session_id.
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', "")
        self.session_id = kwargs.get('session_id', "")
