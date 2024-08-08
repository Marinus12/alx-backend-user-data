#!/usr/bin/env python3
""" Initialization of API views
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import session_auth_views

app_views.register_blueprint(session_auth_views)
