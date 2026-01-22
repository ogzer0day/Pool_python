# SubjectVote Model - ADMIRAL (Subject clarification voting)
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class VoteStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    STAFF_DECIDED = "staff_decided"


class SubjectVote(Base):
    __tablename__ = "subject_votes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(VoteStatus), default=VoteStatus.OPEN)
    winning_option_id = Column(Integer, ForeignKey("vote_options.id"), nullable=True)
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
            "user_id": self.user_id,
            "status": self.status.value if self.status else None,
            "winning_option_id": self.winning_option_id,
            "staff_decision_by": self.staff_decision_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
