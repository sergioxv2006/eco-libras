from models import db
from sqlalchemy.orm import sessionmaker, Session 
from models import Usuario
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

Bcrypt_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


def pegar_session():
    try: 
       Session = sessionmaker(bind= db)
       session = Session()
       yield session
    finally:
       session.close()
