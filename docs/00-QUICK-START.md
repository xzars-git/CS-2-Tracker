# CS2 Tracker - Quick Start Guide

**Get Started in 15 Minutes!**

---

## ⚡ Quick Setup (Local Development)

### Prerequisites:
```bash
✅ Python 3.10+
✅ pip
✅ Git (optional)
✅ Steam API Key (get from: https://steamcommunity.com/dev/apikey)
```

---

## Step 1: Project Setup (2 minutes)

```bash
# Create project folder
mkdir cs2-tracker
cd cs2-tracker

# Create structure
mkdir -p backend/app/api
mkdir -p backend/app/services
mkdir -p frontend/js
mkdir -p docs
```

---

## Step 2: Backend Setup (5 minutes)

### Install Dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)  
source venv/bin/activate

# Create requirements.txt
cat > backend/requirements.txt << EOF
fastapi==0.104.0
sqlalchemy==2.0.23
alembic==1.12.1
httpx==0.25.2
beautifulsoup4==4.12.2
pydantic==2.5.0
pydantic-settings==2.1.0
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
EOF

# Install
pip install -r backend/requirements.txt
```

### Create .env File:
```bash
# backend/.env
STEAM_API_KEY=your_steam_api_key_here
DATABASE_URL=sqlite:///./cs2_tracker.db
SECRET_KEY=your_random_secret_key_12345
```

---

## Step 3: Database Setup (3 minutes)

### Create Models:
Copy `04-Database-Design.md` code into `backend/app/models.py`

### Create Database Connection:
Copy `04-Database-Design.md` code into `backend/app/database.py`

### Initialize Database:
```bash
cd backend

# Init alembic
alembic init alembic

# Edit alembic.ini - set database URL:
# sqlalchemy.url = sqlite:///./cs2_tracker.db

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

---

## Step 4: Backend Routes (3 minutes)

### Create Main App (`backend/app/main.py`):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="CS2 Trading Tracker")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CS2 Tracker API"}

@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

## Step 5: Run Backend (1 minute)

```bash
# From backend folder
uvicorn app.main:app --reload --port 8000
```

✅ **Backend running at:** http://localhost:8000  
✅ **API docs at:** http://localhost:8000/docs

---

## Step 6: Frontend Setup (1 minute)

### Create `frontend/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CS2 Tracker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-8">CS2 Trading Tracker</h1>
        
        <div class="bg-white p-6 rounded-lg shadow">
            <p class="text-xl text-gray-700">Welcome! Your tracker is ready.</p>
            <a href="/docs" class="text-blue-500 hover:underline">View API Docs →</a>
        </div>
    </div>
</body>
</html>
```

---

## Step 7: Run Frontend (1 minute)

```bash
# Open new terminal
cd frontend
python -m http.server 3000
```

✅ **Frontend running at:** http://localhost:3000

---

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] Database file created (`cs2_tracker.db`)
- [ ] Environment variables loaded from `.env`

---

## 🎯 Next Steps

### Phase 1: Add Steam OAuth (Week 1)
1. Read: [`05-Steam-API-Integration.md`](05-Steam-API-Integration.md)
2. Implement Steam login
3. Test with your Steam account

### Phase 2: Add Inventory Sync (Week 1)
1. Read: [`05-Steam-API-Integration.md`](05-Steam-API-Integration.md) (Inventory section)
2. Implement inventory fetch
3. Display items on dashboard

### Phase 3: Add P&L (Week 2)
1. Read: [`09-PnL-Calculation.md`](09-PnL-Calculation.md)
2. Implement trade sync
3. Implement P&L calculation

### Phase 4: Polish & Deploy (Week 3)
1. Read: [`12-Frontend-Design.md`](12-Frontend-Design.md)
2. Improve UI/UX
3. Read: [`15-Deployment-Guide.md`](15-Deployment-Guide.md)
4. Deploy to Railway

---

## 🆘 Troubleshooting

### Backend won't start:
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r backend/requirements.txt

# Check for errors
uvicorn app.main:app --reload
```

### Database errors:
```bash
# Reset database (DEVELOPMENT ONLY!)
rm cs2_tracker.db
alembic upgrade head
```

### Frontend can't connect to backend:
- Check CORS settings in `main.py`
- Verify backend is running on port 8000
- Check browser console for errors

---

## 📚 Additional Resources

- **Full Documentation:** See [`00-MASTER-INDEX.md`](00-MASTER-INDEX.md)
- **Development Roadmap:** See [`01-Project-Overview.md`](01-Project-Overview.md)
- **Deployment Options:** See [`15-Deployment-Guide.md`](15-Deployment-Guide.md)

---

**Happy Coding! 🚀**

Ready to build your CS2 Trading Tracker!
