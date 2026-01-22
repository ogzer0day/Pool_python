# 🛡️ LeetJury - The Peer Consensus Engine

<div align="center">

![LeetJury](https://img.shields.io/badge/LeetJury-Peer%20Consensus%20Engine-00d4aa?style=for-the-badge)
![42 Network](https://img.shields.io/badge/42%20Network-1337%20Students-black?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge)

**A Reddit-style collaborative platform for 42/1337 students navigating the new Python common core.**

[Features](#-features) • [Screenshots](#-screenshots) • [Tech Stack](#️-tech-stack) • [Getting Started](#-getting-started) • [API Documentation](#-api-documentation)

</div>

---

## 🎯 What is LeetJury?

**LeetJury** is a community-driven platform designed specifically for 42/1337 students. It combines the best of Reddit-style discussions with peer evaluation tools to help students:

- 🗳️ **Resolve subject ambiguities** through democratic voting
- ⚔️ **Settle correction disputes** fairly with community input
- 📚 **Share and discover resources** for learning
- 🧪 **Exchange test cases** with quality assurance
- 🔄 **Find peers for mock evaluations** (Recode Me)

### 💡 The Staff Override Principle

What makes LeetJury unique is the **Staff Override** system:
- When a **staff member** makes a decision on any vote or dispute
- The decision is **immediately FINAL**
- Even if 100 students voted differently, staff wins
- This ensures official rulings are always respected

---

## ✨ Features

### 🏠 Feed (Dashboard)
The central hub showing all platform activity in a Reddit-style feed:
- **Latest votes, disputes, resources, and tests** in one place
- **Upvote/downvote** on posts
- **Comment system** for discussions
- **Search functionality** to find specific topics
- **Real-time updates** on new content

### ⚖️ Consensus Court (Subject Votes)
When project subjects are unclear, students create votes to clarify what's allowed:

| Feature | Description |
|---------|-------------|
| **Create Vote** | Post a question about subject interpretation |
| **Multiple Options** | Define possible answers/interpretations |
| **Community Voting** | All students can cast their vote |
| **Staff Decision** | Staff can make final ruling at any time |
| **Vote Expiration** | Automatic closing after deadline |
| **Edit/Delete** | Creators can modify their own posts |

**Example Use Case:**
> "For ft_printf, is it allowed to use malloc in the buffer management?"
> - Option A: Yes, malloc is allowed
> - Option B: No, only stack allocation
> - Staff Decision: Option A ✅

### ⚔️ Live War Room (Disputes)
Real-time correction dispute resolution:

| Feature | Description |
|---------|-------------|
| **Report Dispute** | Describe what happened during evaluation |
| **Two Sides** | Vote for corrector OR corrected |
| **Evidence** | Share screenshots or explanations |
| **Live Voting** | Watch votes come in real-time |
| **Staff Override** | Staff can settle disputes instantly |

**How it works:**
1. Student A corrects Student B
2. Disagreement occurs about a specific point
3. Either student creates a dispute
4. Community votes on who is right
5. Staff can override at any time

### 📁 Resource Vault
A collaborative library of learning materials:

| Feature | Description |
|---------|-------------|
| **Share Links** | Post tutorials, docs, videos, articles |
| **Categorize** | Organize by project |
| **Upvote/Downvote** | Best resources rise to top |
| **Creator Controls** | Edit or delete your submissions |
| **Staff Moderation** | Remove inappropriate content |

**Resource Types:**
- 📖 Documentation & Guides
- 🎥 Video Tutorials
- 📝 Blog Posts & Articles
- 🔗 Useful Tools & Links

### 🧪 Community Tests
A repository of community-contributed test cases:

| Feature | Description |
|---------|-------------|
| **Submit Tests** | Share your GitHub test repos |
| **Staff Approval** | Tests require staff review before publishing |
| **Download Counter** | See how popular tests are |
| **Quality Control** | Reject low-quality submissions |
| **Project Filter** | Find tests for specific projects |

**Workflow:**
1. Student submits test with GitHub URL
2. Staff reviews the submission
3. If approved, test becomes public
4. Other students can download and use it

### 🔄 Recode Me (Mock Evaluations)
Find peers for practice evaluations and recoding sessions:

| Feature | Description |
|---------|-------------|
| **Post Request** | Ask for someone to evaluate your project |
| **Select Project** | Choose which project you need help with |
| **Choose Campus** | Filter by 1337/42 campus |
| **Meeting Platform** | Discord, Google Meet, Zoom, In Person, etc. |
| **Accept Requests** | Help other students by accepting their requests |
| **Status Tracking** | Open → Matched → Completed |

**Available Campuses:**
- 🇲🇦 1337 Khouribga, Ben Guerir, Tetouan, MED, Rabat
- 🇫🇷 42 Paris, Lyon, Nice
- 🇩🇪 42 Berlin
- 🇬🇧 42 London
- 🇯🇵 42 Tokyo
- 🇰🇷 42 Seoul

**Meeting Platforms:**
- 🎮 Discord
- 📹 Google Meet
- 💻 Zoom
- 👥 Microsoft Teams
- 💬 Slack Huddle
- 🏫 In Person

### 👤 Profile
Personal dashboard showing your activity:

| Feature | Description |
|---------|-------------|
| **User Info** | 42 avatar, login, email |
| **Staff Badge** | Special indicator for staff members |
| **Activity Stats** | Your contributions to the platform |
| **My Requests** | Track your recode requests |

---

## 📸 Screenshots

### Dashboard / Feed
```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ LeetJury                           🔍 Search...          │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│ 🏠 Feed      │  [New Post ▼]                               │
│ ⚖️ Consensus │  ┌─────────────────────────────────────┐    │
│ ⚔️ War Room  │  │ 📝 @student1 posted a vote          │    │
│ 🧪 Tests     │  │ "Is malloc allowed in ft_printf?"   │    │
│ 🔄 Recode Me │  │ 👍 42  👎 3  💬 12 comments         │    │
│ 📁 Resources │  └─────────────────────────────────────┘    │
│ 👤 Profile   │                                              │
│              │  ┌─────────────────────────────────────┐    │
│              │  │ ⚔️ @student2 opened a dispute       │    │
│              │  │ "Corrector marked wrong on parsing" │    │
│              │  │ 🅰️ Corrector: 8  🅱️ Corrected: 15  │    │
│              │  └─────────────────────────────────────┘    │
└──────────────┴──────────────────────────────────────────────┘
```

### Recode Me
```
┌─────────────────────────────────────────────────────────────┐
│ 🔄 Recode Me                                                │
│ Find a peer for mock evaluations & recoding sessions        │
├─────────────────────────────────────────────────────────────┤
│ [🔄 Refresh] [📋 My Requests (2)] [+ Post Recode Request]  │
├─────────────────────────────────────────────────────────────┤
│ Project: [All ▼]    Campus: [All ▼]                        │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐│
│ │ 👤 @yelgoumr wants a mock eval                          ││
│ │ 📁 Python Module 00                                     ││
│ │ 🎮 Discord • 📍 1337 Rabat • 🕐 Jan 22                  ││
│ │ "Need help reviewing my module before submission"       ││
│ │                                        [🤝 Accept]      ││
│ └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
|-------|------------|-------------|
| **Frontend** | React 18 + Vite | Fast, modern UI framework |
| **Styling** | TailwindCSS | Utility-first CSS |
| **State** | Zustand | Lightweight state management |
| **Backend** | FastAPI (Python) | High-performance async API |
| **Database** | PostgreSQL (Railway) | Reliable relational database |
| **ORM** | SQLAlchemy (Async) | Python SQL toolkit |
| **Auth** | 42 OAuth API | Native 42 authentication |
| **JWT** | PyJWT | Secure token management |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL database
- 42 API credentials

### 1. Clone the repository
```bash
git clone https://github.com/your-team/1337Jury.git
cd 1337Jury
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Fill in .env with your credentials
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Environment Variables

**Backend `.env`:**
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
FT_CLIENT_ID=your_42_client_id
FT_CLIENT_SECRET=your_42_client_secret
FT_REDIRECT_URI=http://localhost:8000/api/auth/callback
JWT_SECRET=your_super_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400
FRONTEND_URL=http://localhost:5173
```

---

## 📚 API Documentation

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login` | GET | Redirect to 42 OAuth |
| `/api/auth/callback` | GET | Handle OAuth callback |
| `/api/auth/me` | GET | Get current user |

### Projects
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects` | GET | List all projects |
| `/api/projects/{id}` | GET | Get project details |

### Subject Votes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/votes` | GET | List votes |
| `/api/votes` | POST | Create new vote |
| `/api/votes/{id}` | PUT | Update vote (creator) |
| `/api/votes/{id}` | DELETE | Delete vote (staff) |
| `/api/votes/{id}/cast` | POST | Cast your vote |
| `/api/votes/{id}/staff-decision` | POST | Staff override |

### Disputes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/disputes` | GET | List disputes |
| `/api/disputes` | POST | Create dispute |
| `/api/disputes/{id}` | PUT | Update dispute (creator) |
| `/api/disputes/{id}` | DELETE | Delete dispute (staff) |
| `/api/disputes/{id}/vote` | POST | Vote on dispute |
| `/api/disputes/{id}/staff-decision` | POST | Staff override |

### Resources
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/resources` | GET | List resources |
| `/api/resources` | POST | Share resource |
| `/api/resources/{id}/vote` | POST | Upvote/downvote |
| `/api/resources/{id}` | DELETE | Delete resource |

### Tests
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tests` | GET | List approved tests |
| `/api/tests/pending` | GET | Pending tests (staff) |
| `/api/tests` | POST | Submit test |
| `/api/tests/{id}/approve` | POST | Approve test (staff) |
| `/api/tests/{id}/reject` | POST | Reject test (staff) |
| `/api/tests/{id}/download` | POST | Download test |

### Recode Requests
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/recodes` | GET | List open requests |
| `/api/recodes/my` | GET | My requests |
| `/api/recodes/campuses` | GET | Available campuses |
| `/api/recodes/platforms` | GET | Meeting platforms |
| `/api/recodes` | POST | Create request |
| `/api/recodes/{id}/accept` | POST | Accept request |
| `/api/recodes/{id}/complete` | POST | Mark completed |
| `/api/recodes/{id}/cancel` | POST | Cancel request |

---

## 📁 Project Structure

```
LeetJury/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Environment config
│   │   ├── database.py          # Database connection
│   │   ├── api/routes/          # API endpoints
│   │   │   ├── auth.py          # Authentication
│   │   │   ├── projects.py      # Projects
│   │   │   ├── votes.py         # Subject votes
│   │   │   ├── disputes.py      # Correction disputes
│   │   │   ├── resources.py     # Learning resources
│   │   │   ├── tests.py         # Community tests
│   │   │   ├── recodes.py       # Recode requests
│   │   │   └── comments.py      # Comments
│   │   ├── models/              # SQLAlchemy models
│   │   ├── services/            # Business logic
│   │   └── middleware/          # Auth middleware
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/               # React pages
│   │   │   ├── Dashboard.jsx    # Feed/Home
│   │   │   ├── Votes.jsx        # Consensus Court
│   │   │   ├── Disputes.jsx     # Live War Room
│   │   │   ├── Resources.jsx    # Resource Vault
│   │   │   ├── Tests.jsx        # Community Tests
│   │   │   ├── RecodePage.jsx   # Recode Me
│   │   │   └── Profile.jsx      # User Profile
│   │   ├── components/          # Reusable components
│   │   │   └── Layout.jsx       # App layout
│   │   ├── store/               # Zustand state
│   │   └── services/            # API calls
│   │       └── api.js           # Axios client
│   └── package.json
└── README.md
```

---

## 🗄️ Database Schema

| Table | Description |
|-------|-------------|
| `users` | 42 user accounts with staff flag |
| `projects` | Python common core projects |
| `resources` | Learning materials (links) |
| `resource_votes` | Upvotes/downvotes on resources |
| `tests` | Community test cases |
| `subject_votes` | Clarification questions |
| `vote_options` | Answer options for votes |
| `user_votes` | User's cast votes |
| `disputes` | Correction disagreements |
| `dispute_votes` | Votes on disputes |
| `comments` | Discussion comments |
| `recode_requests` | Mock evaluation requests |

---

## 👥 Team

| Developer | Role | Responsibilities |
|-----------|------|------------------|
| **YASSINE** | Backend Dev (Database) | Database setup, schema design |
| **ADMIRAL** | Backend Dev 1 | Auth, Users, Voting, Disputes API |
| **ZERO** | Backend Dev 2 | Resources, Tests API |
| **FATYZA** | Frontend Dev | Complete React UI |

---

## 🏆 Acknowledgments

- **42 Network** for the amazing peer-learning environment
- **1337 School** for pushing us to build real solutions
- All students who will use this platform to help each other

---

<div align="center">

**Built with ❤️ for the 42/1337 community**

[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)](https://1337.ma)

</div>
