# Test Model - ZERO
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    github_url = Column(String(500), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_approved = Column(Boolean, default=False)  # Staff approval
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    downloads = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "github_url": self.github_url,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "is_approved": self.is_approved,
            "downloads": self.downloads,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
