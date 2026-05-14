# backend/app/main.py
# Ponto de entrada da aplicação FastAPI.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import usuarios, perfis

# Cria todas as tabelas no banco ao iniciar (se ainda não existirem)
Base.metadata.create_all(bind=engine)

# Instancia a aplicação
app = FastAPI(
    title="Sistema de Usuários e Perfis",
    description="API REST — Grupo 1 | Serviços de Redes para Internet",
    version="1.0.0",
    root_path="/api",
)

# Permite requisições do frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os roteadores
app.include_router(usuarios.router)
app.include_router(perfis.router)


# Rota raiz — apenas para verificar se a API está no ar
@app.get("/", tags=["Status"])
def status():
    return {"status": "ok", "mensagem": "API funcionando!"}
