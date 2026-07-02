import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import usuarios, perfis
from app.logger import enviar_log

for tentativa in range(10):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except Exception as erro:
        enviar_log(f"Erro ao conectar no PostgreSQL (tentativa {tentativa + 1}): {erro}", "error")
        time.sleep(3)
else:
    enviar_log("Nao foi possivel conectar no PostgreSQL", "error")
    raise SystemExit(1)

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


@app.on_event("startup")
def ao_iniciar():
    enviar_log("Aplicacao FastAPI iniciada", "info")


@app.middleware("http")
async def registrar_requisicao(request: Request, call_next):
    resposta = await call_next(request)
    enviar_log(f"{request.method} {request.url.path} -> {resposta.status_code}", "info")
    return resposta


app.include_router(usuarios.router)
app.include_router(perfis.router)


@app.get("/", tags=["Status"])
def status():
    return {"status": "ok", "mensagem": "API funcionando!"}
