#!/usr/bin/env python3
""" Main auth test
"""
from api.v1.auth.auth import Auth

auth = Auth()

print(auth.require_auth("/api/v1/users", ["/api/v1/stat*"]))  # True
print(auth.require_auth("/api/v1/status", ["/api/v1/stat*"]))  # False
print(auth.require_auth("/api/v1/stats", ["/api/v1/stat*"]))  # False
print(auth.require_auth("/api/v1/statistics", ["/api/v1/stat*"]))  # False
print(auth.require_auth("/api/v1/status", ["/api/v1/status*"]))  # False
print(auth.require_auth("/api/v1/status/health", ["/api/v1/status*"]))  # False
print(auth.require_auth("/api/v1/status", ["/api/v1/status"]))  # False
print(auth.require_auth("/api/v1/users", ["/api/v1/status"]))  # True
print(auth.require_auth(None, ["/api/v1/stat*"]))  # True
print(auth.require_auth("/api/v1/status", None))  # True
print(auth.require_auth("/api/v1/status", []))  # True
