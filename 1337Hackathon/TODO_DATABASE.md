# 🗄️ Database Setup & Structure TODO

**Purpose**: Complete guide for setting up PostgreSQL database and all table structures for 42Nexus
**Assigned to**: Backend Developer 1 (with coordination from all backend devs)

---

## 🚀 Phase 1: PostgreSQL Installation & Setup (1-2 hours)

### Task 1.1: Install PostgreSQL
- [ ] **On Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  ```
- [ ] **On macOS**:
  ```bash
  brew install postgresql@15
  brew services start postgresql@15
  ```
- [ ] Verify installation:
  ```bash
  psql --version
  ```

### Task 1.2: Start PostgreSQL Service
- [ ] Start the service:
  ```bash
  # Ubuntu/Debian
  sudo systemctl start postgresql
  sudo systemctl enable postgresql
  
  # macOS
  brew services start postgresql
  ```
- [ ] Check status:
  ```bash
  sudo systemctl status postgresql
  ```

### Task 1.3: Create Database & User
- [ ] Access PostgreSQL:
  ```bash
  sudo -u postgres psql
  ```
- [ ] Create database and user:
  ```sql
  -- Create the database
  CREATE DATABASE nexus42;
  
  -- Create a user with password
  CREATE USER nexus_admin WITH ENCRYPTED PASSWORD 'your_secure_password_here';
  
  -- Grant all privileges
  GRANT ALL PRIVILEGES ON DATABASE nexus42 TO nexus_admin;
  
  -- Connect to the database
  \c nexus42
  
  -- Grant schema privileges
  GRANT ALL ON SCHEMA public TO nexus_admin;
  
  -- Exit
  \q
  ```

### Task 1.4: Test Connection
- [ ] Test connection with new user:
  ```bash
  psql -h localhost -U nexus_admin -d nexus42
  ```
- [ ] Note your connection string:
  ```
  postgresql://nexus_admin:your_secure_password_here@localhost:5432/nexus42
  ```

**💡 Why**: PostgreSQL is production-ready, supports JSON fields, and works great with SQLAlchemy async.

---

## 📊 Phase 2: Database Schema Design (Reference)

### Complete Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │──────────────────────────────────────┐
│ login           │                                      │
│ email           │                                      │
│ display_name    │                                      │
│ avatar_url      │                                      │
│ role            │                                      │
│ campus_id       │                                      │
│ created_at      │                                      │
│ updated_at      │                                      │
└─────────────────┘                                      │
        │                                                │
        │ 1:N                                            │
        ▼                                                │
┌─────────────────┐       ┌─────────────────┐           │
│   PROJECTS      │       │   RESOURCES     │           │
├─────────────────┤       ├─────────────────┤           │
│ id (PK)         │◄──────│ project_id (FK) │           │
│ name            │       │ user_id (FK)    │───────────┤
│ slug            │       │ id (PK)         │           │
│ description     │       │ title           │           │
│ order_index     │       │ description     │           │
└─────────────────┘       │ url             │           │
        │                 │ resource_type   │           │
        │                 │ created_at      │           │
        │                 │ updated_at      │           │
        │                 └─────────────────┘           │
        │                         │                     │
        │                         │ 1:N                 │
        │                         ▼                     │
        │                 ┌─────────────────┐           │
        │                 │ RESOURCE_VOTES  │           │
        │                 ├─────────────────┤           │
        │                 │ id (PK)         │           │
        │                 │ resource_id(FK) │           │
        │                 │ user_id (FK)    │───────────┤
        │                 │ is_upvote       │           │
        │                 └─────────────────┘           │
        │                                               │
        │                 ┌─────────────────┐           │
        │                 │     TESTS       │           │
        │                 ├─────────────────┤           │
        ├────────────────►│ project_id (FK) │           │
        │                 │ user_id (FK)    │───────────┤
        │                 │ id (PK)         │           │
        │                 │ title           │           │
        │                 │ description     │           │
        │                 │ code            │           │
        │                 │ language        │           │
        │                 │ downloads       │           │
        │                 │ is_approved     │           │
        │                 │ created_at      │           │
        │                 │ updated_at      │           │
        │                 └─────────────────┘           │
        │                                               │
        │                 ┌─────────────────┐           │
        │                 │  SUBJECT_VOTES  │           │
        │                 ├─────────────────┤           │
        ├────────────────►│ project_id (FK) │           │
        │                 │ user_id (FK)    │───────────┤
        │                 │ staff_user_id   │───────────┤
        │                 │ id (PK)         │           │
        │                 │ question        │           │
        │                 │ context         │           │
        │                 │ status          │           │
        │                 │ staff_decision  │           │
        │                 │ created_at      │           │
        │                 │ resolved_at     │           │
        │                 └─────────────────┘           │
        │                         │                     │
        │                         │ 1:N                 │
        │                         ▼                     │
        │                 ┌─────────────────┐           │
        │                 │  VOTE_OPTIONS   │           │
        │                 ├─────────────────┤           │
        │                 │ id (PK)         │           │
        │                 │ subject_vote_id │           │
        │                 │ option_text     │           │
        │                 └─────────────────┘           │
        │                         │                     │
        │                         │ 1:N                 │
        │                         ▼                     │
        │                 ┌─────────────────┐           │
        │                 │   USER_VOTES    │           │
        │                 ├─────────────────┤           │
        │                 │ id (PK)         │           │
        │                 │ subject_vote_id │           │
        │                 │ option_id (FK)  │           │
        │                 │ user_id (FK)    │───────────┤
        │                 │ created_at      │           │
        │                 └─────────────────┘           │
        │                                               │
        │                 ┌─────────────────┐           │
        │                 │    DISPUTES     │           │
        │                 ├─────────────────┤           │
        └────────────────►│ project_id (FK) │           │
                          │ creator_id (FK) │───────────┤
                          │ staff_user_id   │───────────┘
                          │ id (PK)         │
                          │ description     │
                          │ corrector_opinion│
                          │ corrected_opinion│
                          │ urgency         │
                          │ status          │
                          │ winner          │
                          │ created_at      │
                          │ resolved_at     │
                          └─────────────────┘
                                  │
                                  │ 1:N
                                  ▼
                          ┌─────────────────┐
                          │ DISPUTE_VOTES   │
                          ├─────────────────┤
                          │ id (PK)         │
                          │ dispute_id (FK) │
                          │ user_id (FK)    │
                          │ vote_for        │
                          │ created_at      │
                          └─────────────────┘
```

---

## 🛠️ Phase 3: Create Tables with Raw SQL (2-3 hours)

### Task 3.1: Create ENUM Types
- [ ] Create all enum types first:
  ```sql
  -- User roles
  CREATE TYPE user_role AS ENUM ('student', 'staff');
  
  -- Resource types
  CREATE TYPE resource_type AS ENUM ('documentation', 'tutorial', 'video', 'article', 'other');
  
  -- Vote status
  CREATE TYPE vote_status AS ENUM ('open', 'resolved', 'staff_decided');
  
  -- Staff decision for subject votes
  CREATE TYPE staff_decision AS ENUM ('allowed', 'not_allowed');
  
  -- Dispute status
  CREATE TYPE dispute_status AS ENUM ('active', 'resolved', 'staff_decided');
  
  -- Dispute urgency
  CREATE TYPE dispute_urgency AS ENUM ('low', 'medium', 'high');
  
  -- Dispute winner
  CREATE TYPE dispute_winner AS ENUM ('corrector', 'corrected');
  ```

### Task 3.2: Create Users Table
- [ ] Create users table:
  ```sql
  CREATE TABLE users (
      id INTEGER PRIMARY KEY,  -- 42 intra ID (not auto-increment!)
      login VARCHAR(50) UNIQUE NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL,
      display_name VARCHAR(100),
      avatar_url VARCHAR(500),
      role user_role DEFAULT 'student',
      campus_id INTEGER,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Index for faster lookups
  CREATE INDEX idx_users_login ON users(login);
  CREATE INDEX idx_users_role ON users(role);
  ```

**💡 Note**: User `id` comes from 42 API, so it's NOT auto-increment!

### Task 3.3: Create Projects Table
- [ ] Create projects table:
  ```sql
  CREATE TABLE projects (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      slug VARCHAR(100) UNIQUE NOT NULL,
      description TEXT,
      order_index INTEGER DEFAULT 0,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  );
  
  -- Index for slug lookups
  CREATE INDEX idx_projects_slug ON projects(slug);
  ```

### Task 3.4: Create Resources Table
- [ ] Create resources table:
  ```sql
  CREATE TABLE resources (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(200) NOT NULL,
      description TEXT,
      url VARCHAR(500) NOT NULL,
      resource_type resource_type DEFAULT 'other',
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Indexes
  CREATE INDEX idx_resources_project ON resources(project_id);
  CREATE INDEX idx_resources_user ON resources(user_id);
  CREATE INDEX idx_resources_type ON resources(resource_type);
  ```

### Task 3.5: Create Resource Votes Table
- [ ] Create resource_votes table:
  ```sql
  CREATE TABLE resource_votes (
      id SERIAL PRIMARY KEY,
      resource_id INTEGER NOT NULL REFERENCES resources(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      is_upvote BOOLEAN NOT NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      
      -- One vote per user per resource
      UNIQUE(resource_id, user_id)
  );
  
  -- Index for counting votes
  CREATE INDEX idx_resource_votes_resource ON resource_votes(resource_id);
  ```

### Task 3.6: Create Tests Table
- [ ] Create tests table:
  ```sql
  CREATE TABLE tests (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(200) NOT NULL,
      description TEXT,
      code TEXT NOT NULL,
      language VARCHAR(50) DEFAULT 'python',
      downloads INTEGER DEFAULT 0,
      is_approved BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Indexes
  CREATE INDEX idx_tests_project ON tests(project_id);
  CREATE INDEX idx_tests_user ON tests(user_id);
  CREATE INDEX idx_tests_approved ON tests(is_approved);
  ```

### Task 3.7: Create Subject Votes Table
- [ ] Create subject_votes table:
  ```sql
  CREATE TABLE subject_votes (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      question VARCHAR(500) NOT NULL,
      context TEXT,
      status vote_status DEFAULT 'open',
      staff_decision staff_decision,
      staff_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      resolved_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Indexes
  CREATE INDEX idx_subject_votes_project ON subject_votes(project_id);
  CREATE INDEX idx_subject_votes_status ON subject_votes(status);
  CREATE INDEX idx_subject_votes_user ON subject_votes(user_id);
  ```

### Task 3.8: Create Vote Options Table
- [ ] Create vote_options table:
  ```sql
  CREATE TABLE vote_options (
      id SERIAL PRIMARY KEY,
      subject_vote_id INTEGER NOT NULL REFERENCES subject_votes(id) ON DELETE CASCADE,
      option_text VARCHAR(300) NOT NULL
  );
  
  -- Index
  CREATE INDEX idx_vote_options_subject ON vote_options(subject_vote_id);
  ```

### Task 3.9: Create User Votes Table
- [ ] Create user_votes table:
  ```sql
  CREATE TABLE user_votes (
      id SERIAL PRIMARY KEY,
      subject_vote_id INTEGER NOT NULL REFERENCES subject_votes(id) ON DELETE CASCADE,
      option_id INTEGER NOT NULL REFERENCES vote_options(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      
      -- One vote per user per subject vote
      UNIQUE(subject_vote_id, user_id)
  );
  
  -- Indexes
  CREATE INDEX idx_user_votes_subject ON user_votes(subject_vote_id);
  CREATE INDEX idx_user_votes_option ON user_votes(option_id);
  ```

### Task 3.10: Create Disputes Table
- [ ] Create disputes table:
  ```sql
  CREATE TABLE disputes (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      creator_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      description TEXT NOT NULL,
      corrector_opinion TEXT NOT NULL,
      corrected_opinion TEXT NOT NULL,
      urgency dispute_urgency DEFAULT 'medium',
      status dispute_status DEFAULT 'active',
      winner dispute_winner,
      staff_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      resolved_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Indexes
  CREATE INDEX idx_disputes_project ON disputes(project_id);
  CREATE INDEX idx_disputes_status ON disputes(status);
  CREATE INDEX idx_disputes_urgency ON disputes(urgency);
  CREATE INDEX idx_disputes_creator ON disputes(creator_id);
  ```

### Task 3.11: Create Dispute Votes Table
- [ ] Create dispute_votes table:
  ```sql
  CREATE TABLE dispute_votes (
      id SERIAL PRIMARY KEY,
      dispute_id INTEGER NOT NULL REFERENCES disputes(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      vote_for dispute_winner NOT NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      
      -- One vote per user per dispute
      UNIQUE(dispute_id, user_id)
  );
  
  -- Index
  CREATE INDEX idx_dispute_votes_dispute ON dispute_votes(dispute_id);
  ```

---

## 🌱 Phase 4: Seed Initial Data (1 hour)

### Task 4.1: Seed Projects
- [ ] Insert Python common core projects:
  ```sql
  INSERT INTO projects (name, slug, description, order_index) VALUES
  ('Python Module 00', 'python-00', 'Introduction to Python - Basic syntax, variables, and data types', 1),
  ('Python Module 01', 'python-01', 'Objects, Classes, and Object-Oriented Programming', 2),
  ('Python Module 02', 'python-02', 'Data manipulation and processing', 3),
  ('Python Module 03', 'python-03', 'Decorators and advanced functions', 4),
  ('Python Module 04', 'python-04', 'Inheritance and polymorphism', 5),
  ('Starting', 'starting', 'First project - Getting started with 42', 0),
  ('Minishell Python', 'minishell-py', 'Shell implementation in Python', 6),
  ('Django Piscine', 'django-piscine', 'Web development with Django', 7),
  ('ft_transcendence', 'ft-transcendence', 'Final project - Full-stack web application', 8);
  ```

**💡 Note**: Adjust these projects based on actual 42 Python common core curriculum!

### Task 4.2: Create Test Staff User (for development)
- [ ] Insert a test staff user:
  ```sql
  -- Only for development/testing!
  INSERT INTO users (id, login, email, display_name, role) VALUES
  (1, 'staff_test', 'staff@42.fr', 'Staff Test User', 'staff');
  
  -- Test student user
  INSERT INTO users (id, login, email, display_name, role) VALUES
  (2, 'student_test', 'student@student.42.fr', 'Student Test User', 'student');
  ```

---

## 📜 Phase 5: Complete SQL Script (1 hour)

### Task 5.1: Create Full Migration Script
- [ ] Create `database/init.sql` with all tables:
  ```sql
  -- 42Nexus Database Initialization Script
  -- Run this to set up the complete database
  
  -- =====================
  -- 1. DROP EXISTING (for fresh start)
  -- =====================
  DROP TABLE IF EXISTS dispute_votes CASCADE;
  DROP TABLE IF EXISTS disputes CASCADE;
  DROP TABLE IF EXISTS user_votes CASCADE;
  DROP TABLE IF EXISTS vote_options CASCADE;
  DROP TABLE IF EXISTS subject_votes CASCADE;
  DROP TABLE IF EXISTS tests CASCADE;
  DROP TABLE IF EXISTS resource_votes CASCADE;
  DROP TABLE IF EXISTS resources CASCADE;
  DROP TABLE IF EXISTS projects CASCADE;
  DROP TABLE IF EXISTS users CASCADE;
  
  DROP TYPE IF EXISTS dispute_winner CASCADE;
  DROP TYPE IF EXISTS dispute_urgency CASCADE;
  DROP TYPE IF EXISTS dispute_status CASCADE;
  DROP TYPE IF EXISTS staff_decision CASCADE;
  DROP TYPE IF EXISTS vote_status CASCADE;
  DROP TYPE IF EXISTS resource_type CASCADE;
  DROP TYPE IF EXISTS user_role CASCADE;
  
  -- =====================
  -- 2. CREATE ENUM TYPES
  -- =====================
  CREATE TYPE user_role AS ENUM ('student', 'staff');
  CREATE TYPE resource_type AS ENUM ('documentation', 'tutorial', 'video', 'article', 'other');
  CREATE TYPE vote_status AS ENUM ('open', 'resolved', 'staff_decided');
  CREATE TYPE staff_decision AS ENUM ('allowed', 'not_allowed');
  CREATE TYPE dispute_status AS ENUM ('active', 'resolved', 'staff_decided');
  CREATE TYPE dispute_urgency AS ENUM ('low', 'medium', 'high');
  CREATE TYPE dispute_winner AS ENUM ('corrector', 'corrected');
  
  -- =====================
  -- 3. CREATE TABLES
  -- =====================
  
  -- Users (id from 42 API)
  CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      login VARCHAR(50) UNIQUE NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL,
      display_name VARCHAR(100),
      avatar_url VARCHAR(500),
      role user_role DEFAULT 'student',
      campus_id INTEGER,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Projects
  CREATE TABLE projects (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      slug VARCHAR(100) UNIQUE NOT NULL,
      description TEXT,
      order_index INTEGER DEFAULT 0,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  );
  
  -- Resources
  CREATE TABLE resources (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(200) NOT NULL,
      description TEXT,
      url VARCHAR(500) NOT NULL,
      resource_type resource_type DEFAULT 'other',
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Resource Votes
  CREATE TABLE resource_votes (
      id SERIAL PRIMARY KEY,
      resource_id INTEGER NOT NULL REFERENCES resources(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      is_upvote BOOLEAN NOT NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(resource_id, user_id)
  );
  
  -- Tests
  CREATE TABLE tests (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(200) NOT NULL,
      description TEXT,
      code TEXT NOT NULL,
      language VARCHAR(50) DEFAULT 'python',
      downloads INTEGER DEFAULT 0,
      is_approved BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Subject Votes (Clarification Questions)
  CREATE TABLE subject_votes (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      question VARCHAR(500) NOT NULL,
      context TEXT,
      status vote_status DEFAULT 'open',
      staff_decision staff_decision,
      staff_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      resolved_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Vote Options
  CREATE TABLE vote_options (
      id SERIAL PRIMARY KEY,
      subject_vote_id INTEGER NOT NULL REFERENCES subject_votes(id) ON DELETE CASCADE,
      option_text VARCHAR(300) NOT NULL
  );
  
  -- User Votes (on Subject Questions)
  CREATE TABLE user_votes (
      id SERIAL PRIMARY KEY,
      subject_vote_id INTEGER NOT NULL REFERENCES subject_votes(id) ON DELETE CASCADE,
      option_id INTEGER NOT NULL REFERENCES vote_options(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(subject_vote_id, user_id)
  );
  
  -- Disputes
  CREATE TABLE disputes (
      id SERIAL PRIMARY KEY,
      project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
      creator_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      description TEXT NOT NULL,
      corrector_opinion TEXT NOT NULL,
      corrected_opinion TEXT NOT NULL,
      urgency dispute_urgency DEFAULT 'medium',
      status dispute_status DEFAULT 'active',
      winner dispute_winner,
      staff_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      resolved_at TIMESTAMP WITH TIME ZONE
  );
  
  -- Dispute Votes
  CREATE TABLE dispute_votes (
      id SERIAL PRIMARY KEY,
      dispute_id INTEGER NOT NULL REFERENCES disputes(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      vote_for dispute_winner NOT NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(dispute_id, user_id)
  );
  
  -- =====================
  -- 4. CREATE INDEXES
  -- =====================
  CREATE INDEX idx_users_login ON users(login);
  CREATE INDEX idx_users_role ON users(role);
  CREATE INDEX idx_projects_slug ON projects(slug);
  CREATE INDEX idx_resources_project ON resources(project_id);
  CREATE INDEX idx_resources_user ON resources(user_id);
  CREATE INDEX idx_resources_type ON resources(resource_type);
  CREATE INDEX idx_resource_votes_resource ON resource_votes(resource_id);
  CREATE INDEX idx_tests_project ON tests(project_id);
  CREATE INDEX idx_tests_user ON tests(user_id);
  CREATE INDEX idx_tests_approved ON tests(is_approved);
  CREATE INDEX idx_subject_votes_project ON subject_votes(project_id);
  CREATE INDEX idx_subject_votes_status ON subject_votes(status);
  CREATE INDEX idx_subject_votes_user ON subject_votes(user_id);
  CREATE INDEX idx_vote_options_subject ON vote_options(subject_vote_id);
  CREATE INDEX idx_user_votes_subject ON user_votes(subject_vote_id);
  CREATE INDEX idx_user_votes_option ON user_votes(option_id);
  CREATE INDEX idx_disputes_project ON disputes(project_id);
  CREATE INDEX idx_disputes_status ON disputes(status);
  CREATE INDEX idx_disputes_urgency ON disputes(urgency);
  CREATE INDEX idx_disputes_creator ON disputes(creator_id);
  CREATE INDEX idx_dispute_votes_dispute ON dispute_votes(dispute_id);
  
  -- =====================
  -- 5. SEED DATA
  -- =====================
  INSERT INTO projects (name, slug, description, order_index) VALUES
  ('Starting', 'starting', 'First project - Getting started with 42', 0),
  ('Python Module 00', 'python-00', 'Introduction to Python - Basic syntax, variables, and data types', 1),
  ('Python Module 01', 'python-01', 'Objects, Classes, and Object-Oriented Programming', 2),
  ('Python Module 02', 'python-02', 'Data manipulation and processing', 3),
  ('Python Module 03', 'python-03', 'Decorators and advanced functions', 4),
  ('Python Module 04', 'python-04', 'Inheritance and polymorphism', 5),
  ('Minishell Python', 'minishell-py', 'Shell implementation in Python', 6),
  ('Django Piscine', 'django-piscine', 'Web development with Django', 7),
  ('ft_transcendence', 'ft-transcendence', 'Final project - Full-stack web application', 8);
  
  -- Success message
  SELECT 'Database initialized successfully!' AS status;
  ```

### Task 5.2: Run the Script
- [ ] Execute the script:
  ```bash
  psql -h localhost -U nexus_admin -d nexus42 -f database/init.sql
  ```

---

## 🔧 Phase 6: Alembic Setup for Migrations (Optional but Recommended)

### Task 6.1: Initialize Alembic
- [ ] In the backend folder:
  ```bash
  cd backend
  pip install alembic
  alembic init alembic
  ```

### Task 6.2: Configure Alembic
- [ ] Edit `alembic.ini`:
  ```ini
  # Change this line:
  sqlalchemy.url = postgresql://nexus_admin:your_password@localhost:5432/nexus42
  ```
- [ ] Edit `alembic/env.py`:
  ```python
  # Add at the top
  from app.models import Base  # Import your SQLAlchemy Base
  
  # Change target_metadata
  target_metadata = Base.metadata
  ```

### Task 6.3: Create Initial Migration
- [ ] Generate migration:
  ```bash
  alembic revision --autogenerate -m "Initial database schema"
  ```
- [ ] Apply migration:
  ```bash
  alembic upgrade head
  ```

**💡 Why**: Alembic tracks schema changes over time. Good for production deployments.

---

## 📋 Table Summary

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `users` | Store 42 users | id (from 42), login, role |
| `projects` | List of 42 projects | name, slug, order |
| `resources` | Learning materials | title, url, type |
| `resource_votes` | Up/down votes on resources | is_upvote |
| `tests` | Test case repository | code, downloads |
| `subject_votes` | Clarification questions | question, status, staff_decision |
| `vote_options` | Options for each question | option_text |
| `user_votes` | User's vote on questions | option_id |
| `disputes` | Correction disagreements | corrector_opinion, corrected_opinion, winner |
| `dispute_votes` | Votes on disputes | vote_for (corrector/corrected) |

---

## ⚠️ Important Constraints

### Foreign Key Relationships
- All `user_id` fields reference `users(id)`
- All `project_id` fields reference `projects(id)`
- `ON DELETE CASCADE` ensures clean deletion

### Unique Constraints
- `resource_votes`: One vote per user per resource
- `user_votes`: One vote per user per subject question
- `dispute_votes`: One vote per user per dispute

### Staff Override Logic
- `subject_votes.staff_decision`: When set, question is closed
- `subject_votes.staff_user_id`: Who made the decision
- `disputes.winner`: Final decision
- `disputes.staff_user_id`: Who made the decision

---

## ⏱️ Time Estimates

| Phase | Estimated Time |
|-------|---------------|
| PostgreSQL Setup | 1-2 hours |
| Create Tables | 2-3 hours |
| Seed Data | 1 hour |
| Full Script | 1 hour |
| Alembic (optional) | 1 hour |
| **Total** | **6-8 hours** |

---

## 🔍 Useful Commands

```bash
# Connect to database
psql -h localhost -U nexus_admin -d nexus42

# List all tables
\dt

# Describe a table
\d users

# List all types
\dT

# Run SQL file
\i path/to/file.sql

# Exit psql
\q
```

---

## 💡 Tips

1. **Run init.sql first** - It creates everything in one go
2. **Check foreign keys** - Ensure users/projects exist before inserting related data
3. **Use transactions** - Wrap bulk inserts in `BEGIN` / `COMMIT`
4. **Backup often** - `pg_dump nexus42 > backup.sql`
5. **Index wisely** - Added indexes for common query patterns

Good luck! 🚀
