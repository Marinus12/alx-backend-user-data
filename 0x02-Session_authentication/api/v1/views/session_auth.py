#!/usr/bin/env python3
"""
Session Authentication views
"""

from flask import Blueprint, request, jsonify, make_response
from models.user import User


session_auth_views = Blueprint('session_auth_views', __name__,
                               url_prefix='/auth_session')


@session_auth_views.route('/auth_session/login', methods=['POST'],
                           strict_slashes=False)
def login():
    """
    Handles POST requests to /auth_session/login.
    Authenticates the user and creates a session if valid.
    """
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search(email=email)
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@session_auth_views.route('/auth_session/logout', methods=['DELETE'],
                          strict_slashes=False)
def logout():
    """Handles user logout"""
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
