#!/usr/bin/env python3
""" Initialization of API views """
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
session_auth_views = Blueprint('session_auth_views', __name__)

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *
