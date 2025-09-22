import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

class Configuracao:
    """Classe de configuração da aplicação."""

    # Chave secreta para sessões e flash
    SECRET_KEY = os.getenv("SECRET_KEY") or "super-secret-key-123"

    # Lê a variável DATABASE_URL do .env
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Se não houver DATABASE_URL, usa SQLite local
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///meu_banco.db"

    # Desativa o rastreamento de modificações (melhora performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
