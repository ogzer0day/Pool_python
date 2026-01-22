# User Model - ADMIRAL
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    ft_id = Column(Integer, unique=True, nullable=False, index=True)
    login = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "ft_id": self.ft_id,
            "login": self.login,
            "email": self.email,
            "display_name": self.display_name,
            "avatar_url": self.avatar_url,
            "is_staff": self.is_staff,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
