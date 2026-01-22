# 🎨 Frontend Developer TODO

**Developer Role**: Complete UI for 42Nexus
**Tech Stack**: React + Vite + TailwindCSS + Axios
**Time Budget**: ~13-16 hours

---

## 🚀 Phase 1: Setup (1-2 hours)

### Task 1.1: Initialize Project
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install axios react-router-dom zustand
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Task 1.2: Configure Tailwind
- [ ] `tailwind.config.js`:
  ```js
  export default {
    content: ["./index.html", "./src/**/*.{js,jsx}"],
    theme: { extend: {} },
    plugins: [],
  }
  ```
- [ ] `src/index.css`:
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```

### Task 1.3: API Service
- [ ] `src/services/api.js`:
  ```js
  import axios from 'axios';
  const api = axios.create({ baseURL: 'http://localhost:8000/api' });
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  });
  export default api;
  ```

---

## 🔐 Phase 2: Auth (2-3 hours)

### Task 2.1: Auth Store
- [ ] `src/store/authStore.js`:
  ```js
  import { create } from 'zustand';
  import api from '../services/api';

  export const useAuthStore = create((set) => ({
    user: null,
    isLoading: true,
    login: () => { window.location.href = 'http://localhost:8000/api/auth/login'; },
    setToken: (token) => { localStorage.setItem('token', token); },
    fetchUser: async () => {
      try {
        const { data } = await api.get('/auth/me');
        set({ user: data, isLoading: false });
      } catch { set({ user: null, isLoading: false }); }
    },
    logout: () => { localStorage.removeItem('token'); set({ user: null }); },
  }));
  ```

### Task 2.2: Login Page
- [ ] `src/pages/LoginPage.jsx` - Hero + "Login with 42" button

### Task 2.3: Callback Page
- [ ] `src/pages/CallbackPage.jsx` - Extract token, store, redirect

### Task 2.4: App Router
- [ ] `src/App.jsx` with ProtectedRoute

---

## 📊 Phase 3: Layout (2 hours)

### Task 3.1: Sidebar Layout
- [ ] `src/components/Layout.jsx`:
  - Sidebar with nav: Dashboard, Resources, Votes, Disputes, Tests
  - User info + logout
  - Main content area

### Task 3.2: Dashboard
- [ ] `src/pages/Dashboard.jsx` - Welcome + stats cards

---

## 📚 Phase 4: Resources (2-3 hours)

### Task 4.1: Resources Page
- [ ] `src/pages/Resources.jsx`:
  - List resources with upvote/downvote
  - Add resource form
  - Filter by project/type

---

## 🗳️ Phase 5: Votes (2-3 hours)

### Task 5.1: Votes Page
- [ ] `src/pages/Votes.jsx`:
  - List questions with options
  - Progress bars for vote counts
  - Cast vote button
  - **Staff UI**: "Allowed" / "Not Allowed" buttons
  - **STAFF DECIDED** banner when resolved

---

## ⚡ Phase 6: Disputes (2-3 hours)

### Task 6.1: Disputes Page
- [ ] `src/pages/Disputes.jsx`:
  - Two-column: Corrector vs Corrected
  - Vote for either side
  - Urgency badge (color coded)
  - **Staff UI**: "Corrector Wins" / "Corrected Wins"
  - **STAFF DECIDED** banner with winner

---

## 🧪 Phase 7: Tests (2 hours)

### Task 7.1: Tests Page
- [ ] `src/pages/Tests.jsx`:
  - Grid of test cards
  - Code preview
  - Download button
  - Approved badge

---

## 📋 Pages Summary

| Page | Features |
|------|----------|
| Login | Hero, 42 OAuth button |
| Dashboard | Welcome, stats |
| Resources | List, add, vote |
| Votes | Questions, options, staff override |
| Disputes | Corrector vs corrected, staff override |
| Tests | List, download, approve |

---

## ⏱️ Time: 13-16 hours

### Tips
1. **Start with mock data** - Don't wait for backend
2. **Staff UI is KEY** - Make staff actions prominent
3. **Use Tailwind** - Fast styling
4. **Test at /docs** - Backend Swagger for API testing

Good luck! 🚀
