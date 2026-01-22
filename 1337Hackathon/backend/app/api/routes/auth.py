# Auth Routes - ADMIRAL
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.services.ft_api import ft_api
from app.services.jwt_service import create_access_token, verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/login")
async def login():
    return RedirectResponse(url=ft_api.get_authorization_url())


@router.get("/callback")
async def callback(code: str = Query(...), db: AsyncSession = Depends(get_db)):
    # Exchange code for token
    token_data = await ft_api.exchange_code_for_token(code)
    if not token_data or "access_token" not in token_data:
        raise HTTPException(status_code=400, detail="Failed to get token")

    # Get user info from 42 API
    user_info = await ft_api.get_user_info(token_data["access_token"])
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info")

    # Create or update user
    ft_id = user_info.get("id")
    login = user_info.get("login")
    email = user_info.get("email")
    display_name = user_info.get("displayname") or user_info.get("usual_full_name") or login
    image = user_info.get("image", {})
    avatar_url = image.get("link") if isinstance(image, dict) else None
    is_staff = user_info.get("staff?", False)

    result = await db.execute(select(User).where(User.ft_id == ft_id))
    user = result.scalar_one_or_none()

    if user:
        # Update user info but DO NOT change is_staff for existing users
        user.login = login
        user.email = email
        user.display_name = display_name
        user.avatar_url = avatar_url
        # Keep existing is_staff value - don't overwrite!
    else:
        # Only set is_staff from 42 API for NEW users
        user = User(
            ft_id=ft_id, login=login, email=email,
            display_name=display_name, avatar_url=avatar_url, is_staff=is_staff
        )
        db.add(user)

    await db.commit()
    await db.refresh(user)

    # Generate JWT
    jwt_token = create_access_token(data={
        "sub": str(user.id),
        "login": user.login,
        "is_staff": user.is_staff,
    })

    return RedirectResponse(url=f"{settings.FRONTEND_URL}/callback?token={jwt_token}")


@router.get("/me")
async def get_me(token: str = Query(...), db: AsyncSession = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == int(payload.get("sub"))))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.to_dict()


@router.get("/verify")
async def verify(token: str = Query(...)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"valid": True, "user_id": payload.get("sub"), "login": payload.get("login"), "is_staff": payload.get("is_staff")}
