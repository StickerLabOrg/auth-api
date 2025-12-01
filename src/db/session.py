from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import time
import os

# Carregar URL do banco do docker-compose
DATABASE_URL = os.getenv("DATABASE_URL")

# Base declarativa usada pelos models
Base = declarative_base()

# Função para retry ao conectar ao postgres (resolve o erro de Connection Refused)
def create_engine_with_retry(url, retries=20, delay=1):
    for i in range(retries):
        try:
            engine = create_engine(url, pool_pre_ping=True)
            conn = engine.connect()
            conn.close()
            print("[Auth-API] Banco conectado!")
            return engine
        except OperationalError as e:
            print(f"[Auth-API] Tentativa {i+1}/{retries} falhou, aguardando... {e}")
            time.sleep(delay)
    raise Exception("Auth-API não conseguiu conectar ao banco de dados.")

# Cria engine com retry
engine = create_engine_with_retry(DATABASE_URL)

# Criador de sessões
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependency FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
