from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Perfil(Base):
    __tablename__ = "perfis"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String(50), unique=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    usuarios = relationship("Usuario", back_populates="perfil")


class Usuario(Base):
    __tablename__ = "usuarios"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String(100), nullable=False)
    email     = Column(String(150), unique=True, nullable=False)
    senha     = Column(String(255), nullable=False)
    perfil_id = Column(Integer, ForeignKey("perfis.id"), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    perfil = relationship("Perfil", back_populates="usuarios")
