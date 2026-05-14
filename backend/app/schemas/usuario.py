from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    perfil_id: Optional[int] = None


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    perfil_id: Optional[int] = None


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    perfil_id: Optional[int] = None
    perfil_nome: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
