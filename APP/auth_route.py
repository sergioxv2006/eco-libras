import os
from flask import Blueprint, jsonify, request, session
from APP.dependencies import Bcrypt_context, pegar_session
from .extencoes import db
from models import User
from schemas import LoginSchema
from sqlalchemy.orm import Session


auth_route = Blueprint("admin", __name__, url_prefix="/admin")


def autenticar_usuario(user, senha, session): 
     usuario = session.query(User).filter(User.user_admin == user).first()
     if not usuario: 
          return False
     elif not Bcrypt_context.verify(senha, user.senha):
          return False
     return usuario

@auth_route.route("/login", methods=["POST"])
def admin_login(login_schema: LoginSchema, session: Session = pegar_session):
   usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)