from flask import Blueprint, request, jsonify, current_app, render_template, make_response, redirect, url_for
from werkzeug.security import check_password_hash
from .models import User
import jwt
from datetime import datetime, timedelta

rotas_auth = Blueprint("auth", __name__)

@rotas_auth.route("/admin/login-page", methods=["GET"])
def login_page():
    return render_template("admin_login.html")

@rotas_auth.route("/admin/login", methods=["POST"])
def admin_login():
    """
    Accepts JSON (AJAX) or form POST.
    - JSON: returns JSON {access_token, redirect_url}
    - Form: sets HttpOnly cookie and redirects to admin page
    """
    data = request.get_json(silent=True)
    if data:
        username = data.get("username")
        password = data.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

    if not username or not password:
        if request.is_json:
            return jsonify({"success": False, "message": "Username and password are required"}), 400
        return redirect(url_for('auth.login_page'))

    user = User.query.filter_by(user_admin=username).first()
    if not user or not check_password_hash(user.password_admin, password):
        if request.is_json:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
        return redirect(url_for('auth.login_page', failed=1))

    exp = datetime.utcnow() + timedelta(hours=4)
    token = jwt.encode({
        "sub": username,
        "admin": True,
        "exp": exp
    }, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    if request.is_json:
        return jsonify({
            "success": True,
            "access_token": token,
            "token_type": "bearer",
            "expires_at": exp.isoformat(),
            "redirect_url": url_for('admin.pagina_admin')
        })

    resp = make_response(redirect(url_for('admin.pagina_admin')))
    resp.set_cookie('access_token', token, httponly=True, samesite='Lax')
    return resp

@rotas_auth.route("/login", methods=["POST"])
def site_login():
    """
    Handler for login form on the public site (index). Redirects directly to /admin/ with cookie.
    """
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return redirect(url_for('auth.login_page'))

    user = User.query.filter_by(user_admin=username).first()
    if not user or not check_password_hash(user.password_admin, password):
        return redirect(url_for('auth.login_page', failed=1))

    exp = datetime.utcnow() + timedelta(hours=4)
    token = jwt.encode({
        "sub": username,
        "admin": True,
        "exp": exp
    }, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    resp = make_response(redirect(url_for('admin.pagina_admin')))
    resp.set_cookie('access_token', token, httponly=True, samesite='Lax')
    return resp