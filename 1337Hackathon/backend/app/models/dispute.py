# Dispute Model - ADMIRAL (Correction disputes)
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class DisputeStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    STAFF_DECIDED = "staff_decided"


class DisputeWinner(str, enum.Enum):
    CORRECTOR = "corrector"
    CORRECTED = "corrected"


class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    corrector_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    corrected_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(DisputeStatus), default=DisputeStatus.OPEN)
    winner = Column(Enum(DisputeWinner), nullable=True)
    corrector_votes = Column(Integer, default=0)
    corrected_votes = Column(Integer, default=0)
    staff_decision_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    staff_decision_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "project_id": self.project_id,
            "corrector_id": self.corrector_id,
            "corrected_id": self.corrected_id,
            "status": self.status.value if self.status else None,
            "winner": self.winner.value if self.winner else None,
            "corrector_votes": self.corrector_votes,
            "corrected_votes": self.corrected_votes,
            "staff_decision_by": self.staff_decision_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
