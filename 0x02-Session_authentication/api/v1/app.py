#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.views.session_auth import session_auth_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.register_blueprint(session_auth_views, url_prefix='/api/v1/auth_session')
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv('AUTH_TYPE')


if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handle 404 errors.
    Args:
        error: The error object
    Returns:
        A JSON response with a 404 status code.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """
    Handle 401 errors.
    Args:
        error: The error object
    Returns:
        A JSON response with a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Handle 403 errors.
    Args:
        error: The error object
    Returns:
        A JSON response with a 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    Perform actions before each request.
    Checks if the request requires authentication and validates it.
    """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
