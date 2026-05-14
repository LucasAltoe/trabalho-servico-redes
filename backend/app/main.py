from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import usuarios, perfis

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Usuários e Perfis",
    description="API REST — Grupo 1 | Serviços de Redes para Internet",
    version="1.0.0",
    root_path="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(perfis.router)


@app.get("/", tags=["Status"])
def status():
    return {"status": "ok", "mensagem": "API funcionando!"}
