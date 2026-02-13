# 02 - Tech Stack

**CS2 Trading Tracker - Technology Choices**

---

## 2.1 Backend Stack

| Technology | Version | Purpose | Why Chosen |
|-----------|---------|---------|------------|
| **Python** | 3.10+ | Core language | Async support, rich ecosystem |
| **FastAPI** | 0.104+ | Web framework | Modern, fast, auto-docs |
| **SQLAlchemy** | 2.0+ | ORM | Type-safe, migrations support |
| **Alembic** | 1.12+ | DB migrations | Industry standard |
| **httpx** | 0.25+ | HTTP client | Async, modern API |
| **BeautifulSoup4** | 4.12+ | HTML parsing | CSFloat scraping |
| **Pydantic** | 2.5+ | Data validation | Type-safe schemas |

### Backend Installation:
```bash
pip install fastapi==0.104.0
pip install sqlalchemy==2.0.23
pip install alembic==1.12.1
pip install httpx==0.25.2
pip install beautifulsoup4==4.12.2
pip install pydantic==2.5.0
pip install uvicorn[standard]
```

---

## 2.2 Frontend Stack

| Technology | Version | Purpose | Why Chosen |
|-----------|---------|---------|------------|
| **HTML5** | - | Markup | Standard |
| **Tailwind CSS** | 3.3+ | Styling | Modern, utility-first |
| **Alpine.js** | 3.13+ | Reactivity | Lightweight (15KB) |
| **Chart.js** | 4.4+ | Charts | Free, beautiful charts |
| **Axios** | 1.6+ | HTTP client | Clean API calls |

### Frontend Installation (CDN):
```html
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Axios -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

**Kenapa tidak React/Vue?**
- ✅ Lebih simple untuk MVP
- ✅ Zero build process
- ✅ Lebih cepat untuk prototype
- ⏳ Bisa migrate ke React/Vue nanti jika perlu

---

## 2.3 Database

| Option | Use Case | Pros | Cons |
|--------|----------|------|------|
| **SQLite** | Local development | Zero setup, portable | Single-user only |
| **PostgreSQL** | Production | Scalable, robust | Requires hosting |

### Recommendation:
🎯 **Start with SQLite**, migrate to PostgreSQL if needed.

### SQLite Setup:
```python
# database.py
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./cs2_tracker.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

### PostgreSQL Setup (Production):
```python
# database.py
DATABASE_URL = "postgresql://user:password@localhost:5432/cs2_tracker"
engine = create_engine(DATABASE_URL)
```

---

## 2.4 Deployment Options

| Platform | Cost | Pros | Cons |
|----------|------|------|------|
| **Local** | Free | Full control, zero cost | Not accessible remotely |
| **Railway** | Free tier | Easy deploy, Postgres included | 500 hours/month limit |
| **Vercel** | Free tier | Fast CDN, auto-deploy | Backend cold starts |
| **Docker + VPS** | ~$5/mo | Full control, always-on | Requires DevOps knowledge |

### Recommendation by Use Case:

**Personal Use:**
```
Local development (Free)
```

**Share with Friends:**
```
Railway (Free tier - 500 hours/month)
```

**Production App:**
```
Docker + VPS ($5/month DigitalOcean/Hetzner)
```

---

## 2.5 Development Tools

### Required Tools:
```bash
# Python 3.10+
python --version

# pip (package manager)
pip --version

# Git (version control)
git --version

# Code Editor
# VS Code (recommended) atau PyCharm
```

### Optional Tools:
```bash
# Database viewer
DB Browser for SQLite (for SQLite)
pgAdmin (for PostgreSQL)

# API testing
Postman atau Thunder Client (VS Code extension)

# Terminal
Windows Terminal (Windows)
iTerm2 (macOS)
```

---

## 2.6 Project Structure

```
cs2-tracker/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   ├── steam.py
│   │   │   └── csfloat.py
│   │   ├── services/
│   │   │   ├── inventory.py
│   │   │   ├── pnl.py
│   │   │   └── trade_sync.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── config.py
│   │   └── main.py
│   ├── alembic/
│   │   └── versions/
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── dashboard.js
│       └── charts.js
├── docs/
│   └── (modular documentation)
├── .env.example
├── .gitignore
└── README.md
```

---

## 2.7 Environment Setup

### 1. Create `.env` file:
```bash
# .env
STEAM_API_KEY=your_steam_api_key_here
DATABASE_URL=sqlite:///./cs2_tracker.db
SECRET_KEY=your_secret_key_here
```

### 2. Install dependencies:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize database:
```bash
cd backend
alembic upgrade head
```

### 4. Run development server:
```bash
# Backend
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
python -m http.server 3000
```

---

## 2.8 Why These Technologies?

### Python + FastAPI:
✅ **Fast development** with auto-docs  
✅ **Async support** for concurrent API calls  
✅ **Type safety** dengan Pydantic  
✅ **Easy deployment**

### Tailwind + Alpine.js:
✅ **No build process** needed  
✅ **Fast prototyping**  
✅ **Small bundle size** (<50KB total)  
✅ **Modern UI** dengan minimal effort

### SQLite → PostgreSQL:
✅ **Start simple** dengan SQLite  
✅ **Easy migration** ke PostgreSQL  
✅ **Same SQLAlchemy code** untuk both

---

## Next Steps

✅ **Lanjut ke:** [`03-System-Architecture.md`](03-System-Architecture.md) - Pahami arsitektur  
✅ **Alternative:** [`04-Database-Design.md`](04-Database-Design.md) - Design database schema

---

**Ready to code! 💻**
