#!/usr/bin/env python3
""" Module for API authentication management
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """Class to manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required """
        if path is None:
            return Truei
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path if path.endswith('/') else path + '/'
        for excluded_path in excluded_paths:
            excluded_path = (excluded_path + '/' if not
                             excluded_path.endswith('/') else excluded_path)
            if path.startswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get the authorization header """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user """
        return None
