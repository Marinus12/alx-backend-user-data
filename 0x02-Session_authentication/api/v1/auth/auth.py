#!/usr/bin/env python3
"""
Auth module
"""

from typing import List, TypeVar
from flask import request
from os import getenv
import fnmatch


class Auth:
    """
    Auth class that manages the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a given path requires authentication.
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require
            authentication.
        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path = path.rstrip('/')
        for ex_path in excluded_paths:
            ex_path = ex_path.rstrip('/')
            if fnmatch.fnmatch(path, ex_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.
        Args:
            request (Request): The Flask request object.
        Returns:
            str: The Authorization header value if present, otherwise None.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        Args:
            request (Request): The Flask request object.
        Returns:
            TypeVar('User'): The current user if authenticated, otherwise None.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie from the request.
        Args:
            request (flask.Request): The request object containing cookies.
        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
