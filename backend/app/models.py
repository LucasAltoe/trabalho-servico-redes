# backend/app/models.py
# Define as tabelas do banco de dados usando SQLAlchemy.

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Perfil(Base):
    """
    Tabela: perfis
    Exemplos de perfis: Administrador, Editor, Visitante
    """
    __tablename__ = "perfis"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String(50), unique=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento: um perfil pode ter vários usuários
    usuarios = relationship("Usuario", back_populates="perfil")


class Usuario(Base):
    """
    Tabela: usuarios
    Cada usuário pode ter um perfil associado (chave estrangeira).
    """
    __tablename__ = "usuarios"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String(100), nullable=False)
    email     = Column(String(150), unique=True, nullable=False)
    senha     = Column(String(255), nullable=False)
    perfil_id = Column(Integer, ForeignKey("perfis.id"), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento: acessa o objeto Perfil associado
    perfil = relationship("Perfil", back_populates="usuarios")
