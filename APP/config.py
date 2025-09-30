import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

class Configuracao:
    """Classe de configuração da aplicação."""

    # Chave secreta para sessões e flash
    SECRET_KEY = os.getenv("SECRET_KEY") or "super-secret-key-123"

    # Lê a variável DATABASE_URL do ambiente ou usa SQLite como padrão
    DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///data_bank.db"

    # Se não houver DATABASE_URL, usa SQLite local
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///data_bank.db"

    # Banco de dados SQLite local com caminho absoluto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'instance', 'data_bank.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    # Desativa o rastreamento de modificações (melhora performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
