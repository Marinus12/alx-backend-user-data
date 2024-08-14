#!/usr/bin/env python3
"""Authentication file"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt, checkpw
import bcrypt
import uuid


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
            return checkpw(password.encode('utf-8'),
                           user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session for the user.
        Args:
            email (str): The user's email.
        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid.uuid4())
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a user based on the given session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            User: The User object if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session for a user by setting the session ID to None.
        Args:
            user_id (int): The user's ID.
        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                self._db.update_user(user_id=user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the user with the given email.
        Args:
            email (str): The user's email.
        Returns:
            str: The generated reset token.
        Raises:
            ValueError: If the user with the given email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("Email not registered")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the password for the user associated with
        the given reset token.
        Args:
            reset_token (str): The reset token.
            password (str): The new password.
        Returns:
            None
        Raises:
            ValueError: If the reset token is invalid or user does not exist.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if not user:
                raise ValueError("Invalid reset token")
            hashed_password = self._hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=hashed_password.decode('utf-8'),
                    reset_token=None
            )
        except NoResultFound:
            raise ValueError("Invalid reset token")
