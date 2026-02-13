# CS2 Trading Tracker

A web application to track your CS2 inventory value and trading profit/loss in real-time.

## Features

- 🎮 Steam OAuth login integration
- 📊 Real-time inventory tracking with CSFloat prices
- 💰 Automatic P&L calculation (FIFO + unique token matching)
- 📈 Portfolio value over time charts
- 🔄 Multi-account support
- 💯 100% FREE (no paid APIs required)

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- SQLite/PostgreSQL (database)
- httpx (async HTTP client)

**Frontend:**
- HTML5 + Tailwind CSS
- Alpine.js (lightweight reactivity)
- Chart.js (charts)
- Axios (HTTP client)

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Steam API key
# Get key from: https://steamcommunity.com/dev/apikey
```

### 3. Initialize Database

```bash
cd backend
alembic init alembic
# Edit alembic.ini and set: sqlalchemy.url = sqlite:///./cs2_tracker.db
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### 4. Run Backend

```bash
# From backend directory
uvicorn app.main:app --reload --port 8000
```

Backend will be available at:
- http://localhost:8000 (Frontend)
- http://localhost:8000/docs (API Documentation)

## Project Structure

```
cs2-tracker/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── models.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── docs/
│   └── (modular documentation)
├── .env.example
├── .gitignore
└── README.md
```

## Documentation

See the `docs/` folder for detailed documentation:
- `00-MASTER-INDEX.md` - Documentation overview
- `00-QUICK-START.md` - Quick setup guide
- `01-Project-Overview.md` - Project goals and features
- `05-Steam-API-Integration.md` - Steam API integration guide
- `09-PnL-Calculation.md` - P&L calculation logic
- `15-Deployment-Guide.md` - Deployment options

## Development Status

✅ Project structure setup
✅ Database models created
✅ API routes scaffolded
✅ Basic frontend UI
⏳ Steam OAuth integration (coming next)
⏳ Inventory sync
⏳ P&L calculation
⏳ Charts implementation

## Contributing

This is a personal project, but feedback and suggestions are welcome!

## License

MIT License - feel free to use for your own CS2 trading tracking needs.

---

**Happy Trading! 🚀**
