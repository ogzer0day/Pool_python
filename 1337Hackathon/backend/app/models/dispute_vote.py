# DisputeVote Model - ADMIRAL
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, Enum
from sqlalchemy.sql import func
from app.database import Base
from app.models.dispute import DisputeWinner


class DisputeVote(Base):
    __tablename__ = "dispute_votes"

    id = Column(Integer, primary_key=True, index=True)
    dispute_id = Column(Integer, ForeignKey("disputes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vote_for = Column(Enum(DisputeWinner), nullable=False)  # corrector or corrected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('dispute_id', 'user_id', name='unique_dispute_vote'),
    )
