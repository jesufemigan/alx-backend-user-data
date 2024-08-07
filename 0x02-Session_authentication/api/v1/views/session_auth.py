#!/usr/bin/env python3
"""
handles all view for session authentication
"""
import os
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User


@app_views.route('/auth_session/login', method=['POST'], strict_slashes=False)
def login():
    """
    route for login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    user_not_found = {"error": "no user found for this email"}
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(user_not_found), 404
    if len(users) <= 0:
        return jsonify(user_not_found), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', method=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    logout user
    """
    from api.v1.app import auth
    status = auth.destroy_session(request)
    if not status:
        abort(404)
    return jsonify({}), 200
