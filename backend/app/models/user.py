from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, UUID_ID
from app.db.base_class import Base
import datetime

class User(SQLAlchemyBaseUserTable[UUID_ID], Base):
    __tablename__ = "users"

    id: Mapped[UUID_ID] = mapped_column(UUID, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    perfis = relationship("PerfilDeInteresse", back_populates="owner")
    notifications = relationship("Notification", back_populates="user")