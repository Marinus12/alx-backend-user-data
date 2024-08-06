#!/usr/bin/env python3
"""
Basic authentication module
"""

import base64
from api.v1.auth.auth import Auth
from typing import Optional, Tuple, TypeVar
from models.user import User

# Define a TypeVar for the User instance
UserType = TypeVar('UserType', bound=User)

class BasicAuth(Auth):
    """
    Basic authentication class that inherits from Auth.
    """
    def extract_base64_authorization_header(
        self, authorization_header: Optional[str]
    ) -> Optional[str]:
        """
        Extract the Base64 part from the Authorization header
        for Basic Authentication.
        Args:
            authorization_header (Optional[str]):
            The Authorization header as a string.
        Returns:
            Optional[str]: The Base64 part of the Authorization
            header if valid, otherwise None.
        """
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: Optional[str]
    ) -> Optional[str]:
        """
        Decode a Base64 string and return the UTF-8 decoded value.
        Args:
            base64_authorization_header (Optional[str]):
            The Base64 string to decode.
        Returns:
            Optional[str]: The decoded value as a UTF-8 string if valid,
            otherwise None.
        """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract user email and password from the Base64 decoded value.
        Args:
            decoded_base64_authorization_header (Optional[str]):
            The Base64 decoded value containing user credentials.
        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing
            the user email and password if valid, otherwise (None, None).
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
        self, user_email: Optional[str], user_pwd: Optional[str]
    ) -> Optional[UserType]:
        """
        Retrieve a User instance based on email and password.
        Args:
            user_email (Optional[str]): The email of the user.
            user_pwd (Optional[str]): The password of the user.
        Returns:
            Optional[UserType]: The User instance if valid, otherwise None.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        if not users[0].is_valid_password(user_pwd):
            return None
        return users[0]
