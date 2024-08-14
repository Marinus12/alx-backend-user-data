#!/usr/bin/env python3
"""Basic Flask App"""
from flask import Flask, request, jsonify, redirect,  abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """Returns a JSON response with a welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Register a new user with email and password from form data"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(400, description="Missing email or password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify(email=user.email, message="user created"), 201
    except ValueError as e:
        return jsonify(message=str(e)), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Handles user login."""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, description="Missing email or password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        print(f"Session created for email: {email}, session_id: {session_id}")
        return response
    else:
        abort(401, description="Unauthorized")


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Handles user logout."""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        response = redirect("/")
        response.delete_cookie("session_id")
        return response
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Retrieve the profile information for the currently logged-in user.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403, description="Session ID missing")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403, description="Invalid session")


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password():
    """Generates and returns a reset password token for the user
    with the given email."""
    email = request.form.get("email")
    if not email:
        abort(400, description="Missing email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403, description="Email not registered")


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Update the user's password using a reset token."""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if not email or not reset_token or not new_password:
        abort(400, description="Missing email, reset_token, or new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403, description="Invalid reset token")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
