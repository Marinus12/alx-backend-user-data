#!/usr/bin/env python3
"""Authentication file"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt
import bcrypt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Init"""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes a password using bcrypt.
        Args:
            password (str): The password to be hashed.
        Returns:
            bytes: The hashed password as bytes.
        """
        return hashpw(password.encode('utf-8'), gensalt())

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.
        Args:
            email (str): The user's email.
            password (str): The user's password.
        Returns:
            User: The created User object.
        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email,
                                         hashed_password.decode('utf-8'))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login.
        Args:
            email (str): The user's email.
            password (str): The user's password.
        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False
