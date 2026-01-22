# Tests Routes - ZERO
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.test import Test
from app.models.user import User
from app.middleware.auth import get_current_user, get_staff_user
from pydantic import BaseModel

router = APIRouter(prefix="/tests", tags=["Tests"])


class TestCreate(BaseModel):
    title: str
    description: str | None = None
    github_url: str
    project_id: int


@router.get("")
async def list_tests(
    project_id: int | None = None,
    approved_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    query = select(Test)
    if project_id:
        query = query.where(Test.project_id == project_id)
    if approved_only:
        query = query.where(Test.is_approved == True)
    query = query.order_by(Test.downloads.desc())
    result = await db.execute(query)
    return [t.to_dict() for t in result.scalars().all()]


@router.get("/pending")
async def list_pending_tests(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_staff_user)
):
    """Staff only: List tests awaiting approval"""
    result = await db.execute(select(Test).where(Test.is_approved == False))
    return [t.to_dict() for t in result.scalars().all()]


@router.post("")
async def create_test(
    data: TestCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    test = Test(
        title=data.title,
        description=data.description,
        github_url=data.github_url,
        project_id=data.project_id,
        user_id=user.id,
        is_approved=user.is_staff,  # Auto-approve if staff
    )
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return test.to_dict()


@router.post("/{test_id}/approve")
async def approve_test(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_staff_user)
):
    result = await db.execute(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    test.is_approved = True
    test.approved_by = user.id
    await db.commit()
    return {"message": "Test approved"}


@router.post("/{test_id}/reject")
async def reject_test(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_staff_user)
):
    result = await db.execute(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    await db.delete(test)
    await db.commit()
    return {"message": "Test rejected and deleted"}


@router.post("/{test_id}/download")
async def download_test(test_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if not test.is_approved:
        raise HTTPException(status_code=403, detail="Test not approved")

    test.downloads += 1
    await db.commit()
    return {"github_url": test.github_url, "downloads": test.downloads}


@router.delete("/{test_id}")
async def delete_test(
    test_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    result = await db.execute(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if test.user_id != user.id and not user.is_staff:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db.delete(test)
    await db.commit()
    return {"message": "Deleted"}
