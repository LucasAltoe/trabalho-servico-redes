# backend/app/routes/usuarios.py
# Define todas as rotas (endpoints) relacionadas a usuários.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Usuario, Perfil
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioOut

# O prefixo /usuarios é adicionado automaticamente a todas as rotas aqui
router = APIRouter(prefix="/usuarios", tags=["Usuários"])


# Função auxiliar: monta o dicionário de saída incluindo o nome do perfil
def montar_saida(u: Usuario) -> dict:
    return {
        "id": u.id,
        "nome": u.nome,
        "email": u.email,
        "perfil_id": u.perfil_id,
        "perfil_nome": u.perfil.nome if u.perfil else None,
        "criado_em": u.criado_em,
    }


# ── GET /usuarios ──────────────────────────────────────────
@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    """Retorna todos os usuários cadastrados."""
    usuarios = db.query(Usuario).all()
    return [montar_saida(u) for u in usuarios]


# ── GET /usuarios/{id} ────────────────────────────────────
@router.get("/{usuario_id}", response_model=UsuarioOut)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Retorna um único usuário pelo ID."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return montar_saida(usuario)


# ── POST /usuarios ────────────────────────────────────────
@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    """Cadastra um novo usuário."""
    # Verifica se o e-mail já está em uso
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    # Verifica se o perfil informado existe
    if dados.perfil_id:
        if not db.query(Perfil).filter(Perfil.id == dados.perfil_id).first():
            raise HTTPException(status_code=404, detail="Perfil não encontrado")

    usuario = Usuario(**dados.model_dump())
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return montar_saida(usuario)


# ── PUT /usuarios/{id} ────────────────────────────────────
@router.put("/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de um usuário existente."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return montar_saida(usuario)


# ── DELETE /usuarios/{id} ─────────────────────────────────
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Remove um usuário pelo ID."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario)
    db.commit()
