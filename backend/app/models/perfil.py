from sqlalchemy import Column, String, Boolean, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from fastapi_users_db_sqlalchemy import UUID_ID
import datetime

class PerfilDeInteresse(Base):
    __tablename__ = "interest_profiles"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    nome_perfil = Column(String(100), index=True)
    palavras_chave = Column(JSON)
    uf = Column(String(2), nullable=True)
    municipio_ibge = Column(String(10), nullable=True)
    modalidade_contratacao = Column(String(10), nullable=True)
    categoria = Column(String(50), nullable=True)
    prioridade_urgencia = Column(String(20), nullable=False)
    notificacao_push = Column(Boolean, default=False)
    notificacao_email = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    owner = relationship("User", back_populates="perfis")
    notifications = relationship("Notification", back_populates="perfil")
