# 🔧 Backend Developer 2 TODO

**Developer Role**: Resources & Tests Features
**Tech Stack**: FastAPI (Python) + MariaDB + SQLAlchemy
**Time Budget**: ~9-12 hours

---

## 🎯 Your Responsibilities

You build the **content features**:
- Resources Hub - where students share learning materials
- Tests Repository - where students share test cases

---

## ⚠️ Prerequisites

Before starting, get from your team:
- [ ] From **Backend Dev 3**: Database ready with all tables
- [ ] From **Backend Dev 1**: `get_current_user`, `get_current_staff` middleware

---

## 📚 Phase 1: Resource Feature (4-5 hours)

### Task 1.1: Resource Model
- [ ] Create `app/models/resource.py`:
  ```python
  from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
  from sqlalchemy.orm import relationship
  from sqlalchemy.sql import func
  from app.database import Base
  import enum

  class ResourceType(enum.Enum):
      DOCUMENTATION = "documentation"
      TUTORIAL = "tutorial"
      VIDEO = "video"
      ARTICLE = "article"
      OTHER = "other"

  class Resource(Base):
      __tablename__ = "resources"
      
      id = Column(Integer, primary_key=True, autoincrement=True)
      project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
      user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
      title = Column(String(200), nullable=False)
      description = Column(Text)
      url = Column(String(500), nullable=False)
      resource_type = Column(Enum(ResourceType), default=ResourceType.OTHER)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
      
      project = relationship("Project")
      user = relationship("User")
      votes = relationship("ResourceVote", back_populates="resource", cascade="all, delete-orphan")
  ```

### Task 1.2: Resource Vote Model
- [ ] Create `app/models/resource_vote.py`:
  ```python
  from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
  from sqlalchemy.orm import relationship
  from app.database import Base

  class ResourceVote(Base):
      __tablename__ = "resource_votes"
      
      id = Column(Integer, primary_key=True, autoincrement=True)
      resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
      user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
      is_upvote = Column(Boolean, nullable=False)
      
      __table_args__ = (UniqueConstraint('resource_id', 'user_id'),)
      
      resource = relationship("Resource", back_populates="votes")
      user = relationship("User")
  ```

### Task 1.3: Resource Routes
- [ ] Create `app/api/routes/resources.py`:
  ```python
  from fastapi import APIRouter, Depends, HTTPException
  from sqlalchemy.ext.asyncio import AsyncSession
  from sqlalchemy import select
  from sqlalchemy.orm import selectinload
  from typing import Optional
  from app.database import get_db
  from app.models.resource import Resource
  from app.models.resource_vote import ResourceVote
  from app.models.user import User
  from app.middleware.auth import get_current_user

  router = APIRouter(prefix="/resources", tags=["resources"])

  @router.get("/")
  async def list_resources(project_id: Optional[int] = None, resource_type: Optional[str] = None, search: Optional[str] = None, db: AsyncSession = Depends(get_db)):
      query = select(Resource).options(selectinload(Resource.user), selectinload(Resource.project), selectinload(Resource.votes))
      if project_id: query = query.where(Resource.project_id == project_id)
      if resource_type: query = query.where(Resource.resource_type == resource_type)
      if search: query = query.where(Resource.title.ilike(f"%{search}%"))
      result = await db.execute(query.order_by(Resource.created_at.desc()))
      resources = result.scalars().all()
      
      return [{
          "id": r.id, "title": r.title, "description": r.description, "url": r.url,
          "resource_type": r.resource_type.value, "user_login": r.user.login, "project_name": r.project.name,
          "upvotes": sum(1 for v in r.votes if v.is_upvote),
          "downvotes": sum(1 for v in r.votes if not v.is_upvote),
          "created_at": r.created_at
      } for r in resources]

  @router.post("/")
  async def create_resource(project_id: int, title: str, url: str, description: Optional[str] = None, resource_type: str = "other", db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      resource = Resource(project_id=project_id, user_id=current_user.id, title=title, description=description, url=url, resource_type=resource_type)
      db.add(resource)
      await db.commit()
      return {"id": resource.id, "message": "Resource created"}

  @router.post("/{resource_id}/vote")
  async def vote_resource(resource_id: int, is_upvote: bool, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      resource = await db.get(Resource, resource_id)
      if not resource: raise HTTPException(404, "Resource not found")
      
      existing = await db.execute(select(ResourceVote).where(ResourceVote.resource_id == resource_id, ResourceVote.user_id == current_user.id))
      vote = existing.scalar_one_or_none()
      
      if vote:
          if vote.is_upvote == is_upvote:
              await db.delete(vote)  # Toggle off
          else:
              vote.is_upvote = is_upvote  # Change vote
      else:
          db.add(ResourceVote(resource_id=resource_id, user_id=current_user.id, is_upvote=is_upvote))
      
      await db.commit()
      return {"message": "Vote updated"}

  @router.delete("/{resource_id}")
  async def delete_resource(resource_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      resource = await db.get(Resource, resource_id)
      if not resource: raise HTTPException(404, "Resource not found")
      if resource.user_id != current_user.id and current_user.role.value != "staff":
          raise HTTPException(403, "Not authorized")
      await db.delete(resource)
      await db.commit()
      return {"message": "Deleted"}
  ```

---

## 🧪 Phase 2: Tests Feature (4-5 hours)

### Task 2.1: Test Model
- [ ] Create `app/models/test.py`:
  ```python
  from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
  from sqlalchemy.orm import relationship
  from sqlalchemy.sql import func
  from app.database import Base

  class Test(Base):
      __tablename__ = "tests"
      
      id = Column(Integer, primary_key=True, autoincrement=True)
      project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
      user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
      title = Column(String(200), nullable=False)
      description = Column(Text)
      code = Column(Text, nullable=False)
      language = Column(String(50), default="python")
      downloads = Column(Integer, default=0)
      is_approved = Column(Boolean, default=False)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
      
      project = relationship("Project")
      user = relationship("User")
  ```

### Task 2.2: Test Routes
- [ ] Create `app/api/routes/tests.py`:
  ```python
  from fastapi import APIRouter, Depends, HTTPException
  from fastapi.responses import PlainTextResponse
  from sqlalchemy.ext.asyncio import AsyncSession
  from sqlalchemy import select
  from sqlalchemy.orm import selectinload
  from typing import Optional
  from app.database import get_db
  from app.models.test import Test
  from app.models.user import User
  from app.middleware.auth import get_current_user, get_current_staff

  router = APIRouter(prefix="/tests", tags=["tests"])

  @router.get("/")
  async def list_tests(project_id: Optional[int] = None, approved_only: bool = False, db: AsyncSession = Depends(get_db)):
      query = select(Test).options(selectinload(Test.user), selectinload(Test.project))
      if project_id: query = query.where(Test.project_id == project_id)
      if approved_only: query = query.where(Test.is_approved == True)
      result = await db.execute(query.order_by(Test.downloads.desc()))
      tests = result.scalars().all()
      
      return [{
          "id": t.id, "title": t.title, "description": t.description, "language": t.language,
          "downloads": t.downloads, "is_approved": t.is_approved, "user_login": t.user.login,
          "project_name": t.project.name, "code_preview": t.code[:200] + "..." if len(t.code) > 200 else t.code,
          "created_at": t.created_at
      } for t in tests]

  @router.get("/{test_id}")
  async def get_test(test_id: int, db: AsyncSession = Depends(get_db)):
      result = await db.execute(select(Test).options(selectinload(Test.user), selectinload(Test.project)).where(Test.id == test_id))
      test = result.scalar_one_or_none()
      if not test: raise HTTPException(404, "Test not found")
      return {"id": test.id, "title": test.title, "description": test.description, "code": test.code, "language": test.language, "downloads": test.downloads, "user_login": test.user.login, "project_name": test.project.name}

  @router.post("/")
  async def create_test(project_id: int, title: str, code: str, description: Optional[str] = None, language: str = "python", db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      test = Test(project_id=project_id, user_id=current_user.id, title=title, description=description, code=code, language=language)
      db.add(test)
      await db.commit()
      return {"id": test.id, "message": "Test submitted"}

  @router.get("/{test_id}/download")
  async def download_test(test_id: int, db: AsyncSession = Depends(get_db)):
      test = await db.get(Test, test_id)
      if not test: raise HTTPException(404, "Test not found")
      test.downloads += 1
      await db.commit()
      return PlainTextResponse(content=test.code, headers={"Content-Disposition": f"attachment; filename={test.title.replace(' ', '_')}.py"})

  @router.post("/{test_id}/approve")
  async def approve_test(test_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_staff)):
      test = await db.get(Test, test_id)
      if not test: raise HTTPException(404, "Test not found")
      test.is_approved = True
      await db.commit()
      return {"message": "Test approved"}

  @router.delete("/{test_id}")
  async def delete_test(test_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
      test = await db.get(Test, test_id)
      if not test: raise HTTPException(404, "Test not found")
      if test.user_id != current_user.id and current_user.role.value != "staff":
          raise HTTPException(403, "Not authorized")
      await db.delete(test)
      await db.commit()
      return {"message": "Deleted"}
  ```

---

## 🔧 Phase 3: Integration (1-2 hours)

### Task 3.1: Register Routes
- [ ] Tell Backend Dev 1 to add to `main.py`:
  ```python
  from app.api.routes import resources, tests
  app.include_router(resources.router, prefix="/api")
  app.include_router(tests.router, prefix="/api")
  ```

---

## 📋 API Endpoints

### Resources
| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/api/resources` | No |
| POST | `/api/resources` | Yes |
| POST | `/api/resources/{id}/vote` | Yes |
| DELETE | `/api/resources/{id}` | Owner/Staff |

### Tests
| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/api/tests` | No |
| GET | `/api/tests/{id}` | No |
| POST | `/api/tests` | Yes |
| GET | `/api/tests/{id}/download` | No |
| POST | `/api/tests/{id}/approve` | **Staff** |
| DELETE | `/api/tests/{id}` | Owner/Staff |

---

## ⏱️ Time: 9-12 hours

Good luck! 🚀
