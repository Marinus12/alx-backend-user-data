#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

auth = Auth()
hashed_password = auth._hash_password("Hello Holberton")
print(hashed_password)
