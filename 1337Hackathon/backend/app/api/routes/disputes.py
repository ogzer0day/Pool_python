# Disputes Routes - ADMIRAL
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.database import get_db
from app.models.dispute import Dispute, DisputeStatus, DisputeWinner
from app.models.dispute_vote import DisputeVote
from app.models.user import User
from app.middleware.auth import get_current_user, get_staff_user
from pydantic import BaseModel

router = APIRouter(prefix="/disputes", tags=["Disputes"])


class DisputeCreate(BaseModel):
    title: str
    description: str
    project_id: int
    corrector_username: str
    corrected_username: str


class DisputeVoteRequest(BaseModel):
    vote_for: str  # "corrector" or "corrected"


class StaffDecision(BaseModel):
    winner: str  # "corrector" or "corrected"
    reason: str | None = None


@router.get("")
async def list_disputes(
    project_id: int | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = select(Dispute)
    if project_id:
        query = query.where(Dispute.project_id == project_id)
    if status:
        query = query.where(Dispute.status == DisputeStatus(status))
    query = query.order_by(Dispute.created_at.desc())
    result = await db.execute(query)
    disputes = result.scalars().all()
    
    # Resolve usernames for display
    output = []
    for d in disputes:
        dispute_dict = d.to_dict()
        # Only show usernames to the corrector or corrected themselves
        if d.corrector_id == user.id:
            corrector_result = await db.execute(select(User).where(User.id == d.corrector_id))
            corrector = corrector_result.scalar_one_or_none()
            dispute_dict["corrector_username"] = corrector.login if corrector else None
        else:
            dispute_dict["corrector_username"] = None
        
        if d.corrected_id == user.id:
            corrected_result = await db.execute(select(User).where(User.id == d.corrected_id))
            corrected = corrected_result.scalar_one_or_none()
            dispute_dict["corrected_username"] = corrected.login if corrected else None
        else:
            dispute_dict["corrected_username"] = None
        
        output.append(dispute_dict)
    
    return output


@router.get("/{dispute_id}")
async def get_dispute(
    dispute_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    result = await db.execute(select(Dispute).where(Dispute.id == dispute_id))
    dispute = result.scalar_one_or_none()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    dispute_dict = dispute.to_dict()
    
    # Only show usernames to the corrector or corrected themselves
    if dispute.corrector_id == user.id:
        corrector_result = await db.execute(select(User).where(User.id == dispute.corrector_id))
        corrector = corrector_result.scalar_one_or_none()
        dispute_dict["corrector_username"] = corrector.login if corrector else None
    else:
        dispute_dict["corrector_username"] = None
    
    if dispute.corrected_id == user.id:
        corrected_result = await db.execute(select(User).where(User.id == dispute.corrected_id))
        corrected = corrected_result.scalar_one_or_none()
        dispute_dict["corrected_username"] = corrected.login if corrected else None
    else:
        dispute_dict["corrected_username"] = None
    
    return dispute_dict


@router.post("")
async def create_dispute(
    data: DisputeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Resolve usernames to IDs
    corrector_result = await db.execute(select(User).where(User.login == data.corrector_username))
    corrector = corrector_result.scalar_one_or_none()
    if not corrector:
        raise HTTPException(status_code=404, detail=f"Corrector user '{data.corrector_username}' not found")
    
    corrected_result = await db.execute(select(User).where(User.login == data.corrected_username))
    corrected = corrected_result.scalar_one_or_none()
    if not corrected:
        raise HTTPException(status_code=404, detail=f"Corrected user '{data.corrected_username}' not found")
    
    dispute = Dispute(
        title=data.title,
        description=data.description,
        project_id=data.project_id,
        corrector_id=corrector.id,
        corrected_id=corrected.id,
        created_by=user.id,
    )
    db.add(dispute)
    await db.commit()
    await db.refresh(dispute)
    
    dispute_dict = dispute.to_dict()
    # Show usernames to the creator (they just entered them)
    dispute_dict["corrector_username"] = corrector.login if corrector.id == user.id else None
    dispute_dict["corrected_username"] = corrected.login if corrected.id == user.id else None
    
    return dispute_dict


@router.post("/{dispute_id}/vote")
async def vote_dispute(
    dispute_id: int,
    data: DisputeVoteRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    result = await db.execute(select(Dispute).where(Dispute.id == dispute_id))
    dispute = result.scalar_one_or_none()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    if dispute.status != DisputeStatus.OPEN:
        raise HTTPException(status_code=400, detail="Dispute is closed")

    vote_for = DisputeWinner(data.vote_for)

    # Check existing vote
    result = await db.execute(
        select(DisputeVote).where(DisputeVote.dispute_id == dispute_id, DisputeVote.user_id == user.id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        if existing.vote_for == vote_for:
            raise HTTPException(status_code=400, detail="Already voted for this option")
        # Change vote
        if existing.vote_for == DisputeWinner.CORRECTOR:
            dispute.corrector_votes -= 1
            dispute.corrected_votes += 1
        else:
            dispute.corrected_votes -= 1
            dispute.corrector_votes += 1
        existing.vote_for = vote_for
    else:
        # New vote
        vote = DisputeVote(dispute_id=dispute_id, user_id=user.id, vote_for=vote_for)
        db.add(vote)
        if vote_for == DisputeWinner.CORRECTOR:
            dispute.corrector_votes += 1
        else:
            dispute.corrected_votes += 1

    await db.commit()
    await db.refresh(dispute)
    return dispute.to_dict()


@router.post("/{dispute_id}/staff-decision")
async def staff_decision(
    dispute_id: int,
    data: StaffDecision,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_staff_user)
):
    """STAFF OVERRIDE: Staff decision is FINAL regardless of votes"""
    result = await db.execute(select(Dispute).where(Dispute.id == dispute_id))
    dispute = result.scalar_one_or_none()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")

    dispute.status = DisputeStatus.STAFF_DECIDED
    dispute.winner = DisputeWinner(data.winner)
    dispute.staff_decision_by = user.id
    dispute.staff_decision_reason = data.reason
    dispute.closed_at = datetime.now(timezone.utc)

    await db.commit()
    return {"message": "Staff decision applied - THIS IS FINAL", "winner": data.winner}


@router.post("/{dispute_id}/close")
async def close_dispute(
    dispute_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    result = await db.execute(select(Dispute).where(Dispute.id == dispute_id))
    dispute = result.scalar_one_or_none()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    if dispute.created_by != user.id and not user.is_staff:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Determine winner by votes
    if dispute.corrector_votes > dispute.corrected_votes:
        dispute.winner = DisputeWinner.CORRECTOR
    elif dispute.corrected_votes > dispute.corrector_votes:
        dispute.winner = DisputeWinner.CORRECTED
    # If tie, no winner

    dispute.status = DisputeStatus.CLOSED
    dispute.closed_at = datetime.now(timezone.utc)
    await db.commit()
    return {"message": "Dispute closed", "winner": dispute.winner.value if dispute.winner else None}


class DisputeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


@router.put("/{dispute_id}")
async def update_dispute(
    dispute_id: int,
    data: DisputeUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Update a dispute - only the creator can edit"""
    result = await db.execute(select(Dispute).where(Dispute.id == dispute_id))
    dispute = result.scalar_one_or_none()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    if dispute.created_by != user.id:
        raise HTTPException(status_code=403, detail="Only the creator can edit this dispute")
    if dispute.status != DisputeStatus.OPEN:
        raise HTTPException(status_code=400, detail="Cannot edit a closed dispute")

    if data.title:
        dispute.title = data.title
    if data.description:
        dispute.description = data.description

    await db.commit()
    await db.refresh(dispute)
    return dispute.to_dict()


@router.delete("/{dispute_id}")
async def delete_dispute(
    dispute_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_staff_user)
):
    """Delete a dispute - STAFF ONLY"""
    result = await db.execute(select(Dispute).where(Dispute.id == dispute_id))
    dispute = result.scalar_one_or_none()
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")

    # Delete associated votes first
    from sqlalchemy import delete
    await db.execute(delete(DisputeVote).where(DisputeVote.dispute_id == dispute_id))
    await db.delete(dispute)
    await db.commit()
    return {"message": "Dispute deleted"}
