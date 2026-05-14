from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PerfilCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None


class PerfilUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None


class PerfilOut(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
