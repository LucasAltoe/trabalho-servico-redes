# backend/app/schemas/usuario.py
# Schemas definem o formato esperado dos dados que entram e saem da API.

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Dados necessários para criar um usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    perfil_id: Optional[int] = None


# Dados que podem ser atualizados (todos opcionais)
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    perfil_id: Optional[int] = None


# Formato da resposta que a API devolve
class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    perfil_id: Optional[int] = None
    perfil_nome: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
