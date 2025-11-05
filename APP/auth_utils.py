import os
from functools import wraps
from flask import request, jsonify, redirect, url_for, current_app
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

def _jwt_secret():
    return (current_app.config.get("JWT_SECRET_KEY")
            or current_app.config.get("SECRET_KEY")
            or os.environ.get("JWT_SECRET_KEY")
            or os.environ.get("SECRET_KEY")
            or "change-me")

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"success": False, "message": "Token ausente ou inválido."}), 401
        token = parts[1]
        try:
            payload = jwt.decode(token, _jwt_secret(), algorithms=["HS256"])
        except ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expirado."}), 401
        except InvalidTokenError:
            return jsonify({"success": False, "message": "Token inválido."}), 401
        if not payload.get("admin"):
            return jsonify({"success": False, "message": "Permissão negada."}), 403
        g.jwt_payload = payload
        return func(*args, **kwargs)
    return wrapper

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Prefer cookie (browser form login), fallback to Authorization header (API/AJAX)
        if 'access_token' in request.cookies:
            token = request.cookies.get('access_token')
        elif request.headers.get('Authorization'):
            auth = request.headers.get('Authorization')
            parts = auth.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            if request.accept_mimetypes.accept_html:
                return redirect(url_for('auth.login_page'))
            return jsonify({"success": False, "message": "Token is missing"}), 401

        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            request.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            if request.accept_mimetypes.accept_html:
                return redirect(url_for('auth.login_page'))
            return jsonify({"success": False, "message": "Token expired"}), 401
        except Exception:
            if request.accept_mimetypes.accept_html:
                return redirect(url_for('auth.login_page'))
            return jsonify({"success": False, "message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated