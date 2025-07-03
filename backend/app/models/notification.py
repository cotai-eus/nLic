from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    profile_id = Column(UUID, ForeignKey("interest_profiles.id"))
    numero_controle_pncp = Column(String(50), index=True) # ID da oportunidade no PNCP
    tipo = Column(String(10), nullable=False) # 'push' or 'email'
    enviado_em = Column(DateTime, default=datetime.datetime.now)
    status = Column(String(20), default='sent') # 'sent', 'failed', 'pending'
    conteudo = Column(JSONB, nullable=True)

    user = relationship("User", back_populates="notifications")
    perfil = relationship("app.models.perfil.PerfilDeInteresse", back_populates="notifications")

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(UUID, ForeignKey("notifications.id"))
    log = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    notification = relationship("Notification")

class ApiCallLog(Base):
    __tablename__ = "api_call_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255), nullable=False)
    params = Column(JSONB, nullable=True)
    response_status = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)