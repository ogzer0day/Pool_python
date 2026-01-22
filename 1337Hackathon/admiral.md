# 🔧 Backend Developer 1 TODO

**Developer Role**: Authentication, Users, Voting System & Live Disputes
**Tech Stack**: FastAPI (Python) + MariaDB + SQLAlchemy
**Time Budget**: ~11-16 hours

---

## 🎯 Your Responsibilities

You handle **user-facing interactive features**:
- 42 OAuth Authentication
- User Management
- Subject Clarification Voting
- Live Correction Disputes

**CRITICAL**: Voting & Disputes have **Staff Override** - when staff votes, the decision is FINAL.

---

## ⚠️ Prerequisites (from Backend Dev 3)

Before starting, make sure Backend Dev 3 has:
- [ ] MariaDB database created
- [ ] All tables created
- [ ] Database connection string ready

---

## 🚀 Phase 1: Project Setup (1-2 hours)

### Task 1.1: Initialize FastAPI Project
- [ ] Create project structure:
  ```
  backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── config.py
  │   ├── database.py
  │   ├── api/routes/
  │   ├── models/
  │   ├── schemas/
  │   ├── services/
  │   └── middleware/
  ├── requirements.txt
  └── .env
  ```

### Task 1.2: Install Dependencies
- [ ] Create `requirements.txt`:
  ```
  fastapi==0.104.1
  uvicorn==0.24.0
  sqlalchemy==2.0.23
  aiomysql==0.2.0
  python-dotenv==1.0.0
  httpx==0.25.2
  python-jose[cryptography]==3.3.0
  pydantic==2.5.2
  pydantic-settings==2.1.0
  python-multipart==0.0.6
  ```
- [ ] Install: `pip install -r requirements.txt`

### Task 1.3: Configuration
- [ ] Create `app/config.py`:
  ```python
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      DATABASE_URL: str
      FT_CLIENT_ID: str
      FT_CLIENT_SECRET: str
      FT_REDIRECT_URI: str
      JWT_SECRET: str
      JWT_ALGORITHM: str = "HS256"
      JWT_EXPIRATION: int = 86400
      
      class Config:
          env_file = ".env"

  settings = Settings()
  ```

### Task 1.4: Database Connection
- [ ] Create `app/database.py`:
  ```python
  from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
  from sqlalchemy.orm import sessionmaker, declarative_base
  from app.config import settings

  engine = create_async_engine(settings.DATABASE_URL, echo=True)
  AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
  Base = declarative_base()

  async def get_db():
      async with AsyncSessionLocal() as session:
          yield session
  ```

---

## 🔐 Phase 2: Authentication (3-4 hours)

### Task 2.1: User Model
- [ ] Create `app/models/user.py`:
  ```python
  from sqlalchemy import Column, Integer, String, DateTime, Enum
  from sqlalchemy.sql import func
  from app.database import Base
  import enum

  class UserRole(enum.Enum):
      STUDENT = "student"
      STAFF = "staff"

  class User(Base):
      __tablename__ = "users"
      
      id = Column(Integer, primary_key=True)
      login = Column(String(50), unique=True, nullable=False)
      email = Column(String(255), unique=True, nullable=False)
      display_name = Column(String(100))
      avatar_url = Column(String(500))
      role = Column(Enum(UserRole), default=UserRole.STUDENT)
      campus_id = Column(Integer)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
      updated_at = Column(DateTime(timezone=True), onupdate=func.now())
  ```

### Task 2.2: 42 API Service
- [ ] Create `app/services/ft_api.py`:
  ```python
  import httpx
  from app.config import settings

  FT_AUTH_URL = "https://api.intra.42.fr/oauth/authorize"
  FT_TOKEN_URL = "https://api.intra.42.fr/oauth/token"
  FT_USER_URL = "https://api.intra.42.fr/v2/me"

  def get_authorization_url() -> str:
      params = {
          "client_id": settings.FT_CLIENT_ID,
          "redirect_uri": settings.FT_REDIRECT_URI,
          "response_type": "code",
          "scope": "public"
      }
      return f"{FT_AUTH_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

  async def exchange_code_for_token(code: str) -> dict:
      async with httpx.AsyncClient() as client:
          response = await client.post(FT_TOKEN_URL, data={
              "grant_type": "authorization_code",
              "client_id": settings.FT_CLIENT_ID,
              "client_secret": settings.FT_CLIENT_SECRET,
              "code": code,
              "redirect_uri": settings.FT_REDIRECT_URI
          })
          return response.json()

  async def get_user_info(access_token: str) -> dict:
      async with httpx.AsyncClient() as client:
          response = await client.get(FT_USER_URL, headers={"Authorization": f"Bearer {access_token}"})
          return response.json()
  ```

### Task 2.3: JWT Service
- [ ] Create `app/services/jwt_service.py`:
  ```python
  from datetime import datetime, timedelta
  from jose import jwt, JWTError
  from app.config import settings

  def create_access_token(user_id: int) -> str:
      expire = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION)
      return jwt.encode({"sub": str(user_id), "exp": expire}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

  def verify_token(token: str) -> int | None:
      try:
          payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
          return int(payload.get("sub"))
      except JWTError:
          return None
  ```

### Task 2.4: Auth Middleware
- [ ] Create `app/middleware/auth.py`:
  ```python
  from fastapi import Depends, HTTPException
  from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
  from sqlalchemy.ext.asyncio import AsyncSession
  from typing import Optional
  from app.database import get_db
  from app.services.jwt_service import verify_token
  from app.models.user import User, UserRole

  security = HTTPBearer()
  optional_security = HTTPBearer(auto_error=False)

  async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
      user_id = verify_token(credentials.credentials)
      if not user_id:
          raise HTTPException(status_code=401, detail="Invalid token")
      user = await db.get(User, user_id)
      if not user:
          raise HTTPException(status_code=404, detail="User not found")
      return user

  async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security), db: AsyncSession = Depends(get_db)) -> Optional[User]:
      if not credentials:
          return None
      user_id = verify_token(credentials.credentials)
      return await db.get(User, user_id) if user_id else None

  async def get_current_staff(current_user: User = Depends(get_current_user)) -> User:
      if current_user.role != UserRole.STAFF:
          raise HTTPException(status_code=403, detail="Staff access required")
      return current_user
  ```

### Task 2.5: Auth Routes
- [ ] Create `app/api/routes/auth.py`:
  ```python
  from fastapi import APIRouter, Depends, HTTPException
  from fastapi.responses import RedirectResponse
  from sqlalchemy.ext.asyncio import AsyncSession
  from app.database import get_db
  from app.services import ft_api, jwt_service
  from app.models.user import User, UserRole
  from app.middleware.auth import get_current_user

  router = APIRouter(prefix="/auth", tags=["auth"])

  @router.get("/login")
  async def login():
      return RedirectResponse(ft_api.get_authorization_url())

  @router.get("/callback")
  async def callback(code: str, db: AsyncSession = Depends(get_db)):
      token_data = await ft_api.exchange_code_for_token(code)
      if "error" in token_data:
          raise HTTPException(status_code=400, detail="Failed to get token")
      
      user_info = await ft_api.get_user_info(token_data["access_token"])
      user = await db.get(User, user_info["id"])
      if not user:
          user = User(
              id=user_info["id"], login=user_info["login"], email=user_info["email"],
              display_name=user_info.get("displayname"),
              avatar_url=user_info.get("image", {}).get("link"),
              role=UserRole.STAFF if user_info.get("staff?") else UserRole.STUDENT,
              campus_id=user_info.get("campus", [{}])[0].get("id")
          )
          db.add(user)
      await db.commit()
      return RedirectResponse(f"http://localhost:5173/auth/callback?token={jwt_service.create_access_token(user.id)}")

  @router.get("/me")
  async def get_me(current_user: User = Depends(get_current_user)):
      return {"id": current_user.id, "login": current_user.login, "email": current_user.email, "role": current_user.role.value, "avatar_url": current_user.avatar_url}
  ```

---

## 🗳️ Phase 3: Subject Voting (3-4 hours)

### Task 3.1: Voting Models
- [ ] Create `app/models/subject_vote.py`, `app/models/vote_option.py`, `app/models/user_vote.py` (models matching the database tables)

### Task 3.2: Voting Routes
- [ ] Create `app/api/routes/votes.py`:
  ```python
  from fastapi import APIRouter, Depends, HTTPException
  from sqlalchemy.ext.asyncio import AsyncSession
  from sqlalchemy import select
  from sqlalchemy.orm import selectinload
  from typing import Optional
  from datetime import datetime
  from app.database import get_db
  from app.models.subject_vote import SubjectVote, VoteStatus
  from app.models.vote_option import VoteOption
  from app.models.user_vote import UserVote
  from app.models.user import User
  from app.middleware.auth import get_current_user, get_current_user_optional, get_current_staff

  router = APIRouter(prefix="/votes", tags=["votes"])

  @router.get("/")
  async def list_votes(project_id: Optional[int] = None, status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
      query = select(SubjectVote).options(selectinload(SubjectVote.options).selectinload(VoteOption.user_votes))
      if project_id: query = query.where(SubjectVote.project_id == project_id)
      if status: query = query.where(SubjectVote.status == status)
      result = await db.execute(query.order_by(SubjectVote.created_at.desc()))
      return result.scalars().all()

  @router.post("/")
  async def create_vote(project_id: int, question: str, options: list[str], context: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      if len(options) < 2: raise HTTPException(400, "At least 2 options required")
      vote = SubjectVote(project_id=project_id, user_id=current_user.id, question=question, context=context)
      db.add(vote)
      await db.flush()
      for opt in options: db.add(VoteOption(subject_vote_id=vote.id, option_text=opt))
      await db.commit()
      return {"id": vote.id}

  @router.post("/{vote_id}/vote")
  async def cast_vote(vote_id: int, option_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      vote = await db.get(SubjectVote, vote_id)
      if not vote or vote.status != VoteStatus.OPEN: raise HTTPException(400, "Vote not open")
      existing = await db.execute(select(UserVote).where(UserVote.subject_vote_id == vote_id, UserVote.user_id == current_user.id))
      if existing.scalar_one_or_none(): raise HTTPException(400, "Already voted")
      db.add(UserVote(subject_vote_id=vote_id, option_id=option_id, user_id=current_user.id))
      await db.commit()
      return {"message": "Vote recorded"}

  @router.post("/{vote_id}/staff-decide")
  async def staff_decide(vote_id: int, decision: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_staff)):
      vote = await db.get(SubjectVote, vote_id)
      if not vote: raise HTTPException(404, "Vote not found")
      vote.status = VoteStatus.STAFF_DECIDED
      vote.staff_decision = decision
      vote.staff_user_id = current_user.id
      vote.resolved_at = datetime.utcnow()
      await db.commit()
      return {"message": "Staff decision recorded"}
  ```

---

## ⚡ Phase 4: Live Disputes (3-4 hours)

### Task 4.1: Dispute Models
- [ ] Create `app/models/dispute.py`, `app/models/dispute_vote.py`

### Task 4.2: Dispute Routes
- [ ] Create `app/api/routes/disputes.py`:
  ```python
  from fastapi import APIRouter, Depends, HTTPException
  from sqlalchemy.ext.asyncio import AsyncSession
  from sqlalchemy import select
  from sqlalchemy.orm import selectinload
  from typing import Optional
  from datetime import datetime
  from app.database import get_db
  from app.models.dispute import Dispute, DisputeStatus
  from app.models.dispute_vote import DisputeVote
  from app.models.user import User
  from app.middleware.auth import get_current_user, get_current_staff

  router = APIRouter(prefix="/disputes", tags=["disputes"])

  @router.get("/")
  async def list_disputes(project_id: Optional[int] = None, status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
      query = select(Dispute).options(selectinload(Dispute.votes))
      if project_id: query = query.where(Dispute.project_id == project_id)
      if status: query = query.where(Dispute.status == status)
      result = await db.execute(query.order_by(Dispute.created_at.desc()))
      return result.scalars().all()

  @router.post("/")
  async def create_dispute(project_id: int, description: str, corrector_opinion: str, corrected_opinion: str, urgency: str = "medium", db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      dispute = Dispute(project_id=project_id, creator_id=current_user.id, description=description, corrector_opinion=corrector_opinion, corrected_opinion=corrected_opinion, urgency=urgency)
      db.add(dispute)
      await db.commit()
      return {"id": dispute.id}

  @router.post("/{dispute_id}/vote")
  async def vote_dispute(dispute_id: int, vote_for: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      dispute = await db.get(Dispute, dispute_id)
      if not dispute or dispute.status != DisputeStatus.ACTIVE: raise HTTPException(400, "Dispute not active")
      existing = await db.execute(select(DisputeVote).where(DisputeVote.dispute_id == dispute_id, DisputeVote.user_id == current_user.id))
      if existing.scalar_one_or_none(): raise HTTPException(400, "Already voted")
      db.add(DisputeVote(dispute_id=dispute_id, user_id=current_user.id, vote_for=vote_for))
      await db.commit()
      return {"message": "Vote recorded"}

  @router.post("/{dispute_id}/staff-decide")
  async def staff_decide_dispute(dispute_id: int, winner: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_staff)):
      dispute = await db.get(Dispute, dispute_id)
      if not dispute: raise HTTPException(404, "Dispute not found")
      dispute.status = DisputeStatus.STAFF_DECIDED
      dispute.winner = winner
      dispute.staff_user_id = current_user.id
      dispute.resolved_at = datetime.utcnow()
      await db.commit()
      return {"message": "Staff decision recorded", "winner": winner}
  ```

---

## 🔧 Phase 5: Main App (1 hour)

### Task 5.1: Project Model & Routes
- [ ] Create `app/models/project.py` and `app/api/routes/projects.py`

### Task 5.2: Main App
- [ ] Create `app/main.py`:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  from app.api.routes import auth, projects, votes, disputes

  app = FastAPI(title="42Nexus API")
  app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

  app.include_router(auth.router, prefix="/api")
  app.include_router(projects.router, prefix="/api")
  app.include_router(votes.router, prefix="/api")
  app.include_router(disputes.router, prefix="/api")
  # Backend Dev 2 adds: resources, tests

  @app.get("/health")
  async def health(): return {"status": "healthy"}
  ```

---

## 📋 API Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/api/auth/login` | No |
| GET | `/api/auth/callback` | No |
| GET | `/api/auth/me` | Yes |
| GET | `/api/projects` | No |
| GET/POST | `/api/votes` | Optional/Yes |
| POST | `/api/votes/{id}/vote` | Yes |
| POST | `/api/votes/{id}/staff-decide` | **Staff** |
| GET/POST | `/api/disputes` | Optional/Yes |
| POST | `/api/disputes/{id}/vote` | Yes |
| POST | `/api/disputes/{id}/staff-decide` | **Staff** |

---

## ⏱️ Time: 11-16 hours

Good luck! 🚀
