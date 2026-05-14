# backend/app/routes/perfis.py
# Define todas as rotas (endpoints) relacionadas a perfis.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Perfil
from app.schemas.perfil import PerfilCreate, PerfilUpdate, PerfilOut

router = APIRouter(prefix="/perfis", tags=["Perfis"])


# ── GET /perfis ───────────────────────────────────────────
@router.get("/", response_model=List[PerfilOut])
def listar_perfis(db: Session = Depends(get_db)):
    """Retorna todos os perfis cadastrados."""
    return db.query(Perfil).all()


# ── GET /perfis/{id} ──────────────────────────────────────
@router.get("/{perfil_id}", response_model=PerfilOut)
def obter_perfil(perfil_id: int, db: Session = Depends(get_db)):
    """Retorna um único perfil pelo ID."""
    perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return perfil


# ── POST /perfis ──────────────────────────────────────────
@router.post("/", response_model=PerfilOut, status_code=status.HTTP_201_CREATED)
def criar_perfil(dados: PerfilCreate, db: Session = Depends(get_db)):
    """Cadastra um novo perfil."""
    if db.query(Perfil).filter(Perfil.nome == dados.nome).first():
        raise HTTPException(status_code=400, detail="Perfil com este nome já existe")
    perfil = Perfil(**dados.model_dump())
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil


# ── PUT /perfis/{id} ──────────────────────────────────────
@router.put("/{perfil_id}", response_model=PerfilOut)
def atualizar_perfil(perfil_id: int, dados: PerfilUpdate, db: Session = Depends(get_db)):
    """Atualiza um perfil existente."""
    perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(perfil, campo, valor)
    db.commit()
    db.refresh(perfil)
    return perfil


# ── DELETE /perfis/{id} ───────────────────────────────────
@router.delete("/{perfil_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_perfil(perfil_id: int, db: Session = Depends(get_db)):
    """Remove um perfil pelo ID."""
    perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    db.delete(perfil)
    db.commit()
