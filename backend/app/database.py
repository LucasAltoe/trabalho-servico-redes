import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def ler_senha():
    caminho_secret = "/run/secrets/db_password"
    if os.path.exists(caminho_secret):
        with open(caminho_secret) as arquivo:
            return arquivo.read().strip()
    return os.getenv("POSTGRES_PASSWORD", "postgres")


POSTGRES_USER     = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = ler_senha()
POSTGRES_HOST     = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB       = os.getenv("POSTGRES_DB", "usuarios_db")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
