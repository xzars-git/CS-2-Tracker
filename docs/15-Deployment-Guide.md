# 15 - Deployment Guide

**CS2 Trading Tracker - Deployment Options**

---

## Option 1: Local Development (Free)

### Step 1: Setup Environment
```bash
# Clone/navigate to project
cd cs2-tracker

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 2: Configure Environment Variables
```bash
# Create .env file
STEAM_API_KEY=your_steam_api_key_here
DATABASE_URL=sqlite:///./cs2_tracker.db
SECRET_KEY=your_random_secret_key_here
```

### Step 3: Initialize Database
```bash
cd backend
alembic upgrade head
```

### Step 4: Run Backend
```bash
# From backend directory
uvicorn app.main:app --reload --port 8000

# Backend will run on: http://localhost:8000
```

### Step 5: Run Frontend
```bash
# Open new terminal
cd frontend
python -m http.server 3000

# Frontend will run on: http://localhost:3000
```

---

## Option 2: Railway (Free Tier)

### Why Railway?
- ✅ Free tier (500 hours/month)
- ✅ PostgreSQL included (free 1GB)
- ✅ Auto-deploy from GitHub
- ✅ Zero DevOps setup

### Step 1: Prepare Project Files

**Create `Procfile`:**
```
web: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

**Create `runtime.txt`:**
```
python-3.10.8
```

**Create `railway.json`:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy to Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to GitHub repo (optional)
railway link

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
```

### Step 3: Set Environment Variables
```bash
# In Railway dashboard or CLI
railway variables set STEAM_API_KEY=your_key_here
railway variables set SECRET_KEY=your_secret_key
# DATABASE_URL will be auto-set by Railway
```

### Step 4: Run Migrations
```bash
railway run alembic upgrade head
```

### Step 5: Access Your App
```
Your app will be available at:
https://your-app-name.up.railway.app
```

---

## Option 3: Docker + VPS ($5/month)

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ ./backend/
COPY frontend/ ./frontend/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/cs2_tracker
      - STEAM_API_KEY=${STEAM_API_KEY}
    depends_on:
      - db
    volumes:
      - ./backend:/app/backend
      - ./frontend:/app/frontend
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=cs2_tracker
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Step 3: Deploy to VPS
```bash
# SSH to your VPS
ssh user@your-vps-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose

# Clone your repo
git clone https://github.com/yourusername/cs2-tracker.git
cd cs2-tracker

# Create .env file
nano .env
# Add: STEAM_API_KEY=your_key_here

# Build and run
docker-compose up -d

# Run migrations
docker-compose exec app alembic upgrade head
```

### Step 4: Setup Nginx (Optional)
```bash
# Install Nginx
sudo apt install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/cs2tracker
```

**Nginx Config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/cs2tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Option 4: Vercel (Free Tier)

### For Frontend Only:
```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend folder
cd frontend

# Deploy
vercel
```

### For Full Stack (Serverless):
- Frontend → Vercel
- Backend → Railway/Render
- Use environment variables for backend URL

---

## Comparison Table

| Option | Cost | Ease | Performance | Recommendation |
|--------|------|------|-------------|----------------|
| **Local** | Free | Easy | Good | Development only |
| **Railway** | Free | Very Easy | Good | Personal use |
| **Docker + VPS** | $5/mo | Medium | Excellent | Production |
| **Vercel + Railway** | Free | Easy | Good | Hybrid approach |

---

## Post-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Steam API key working
- [ ] HTTPS enabled (production)
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] Logs accessible
- [ ] Backups configured (for VPS)
- [ ] Domain configured (optional)
- [ ] SSL certificate (Let's Encrypt)

---

## Monitoring & Logs

### Railway:
```bash
# View logs
railway logs

# Monitor app
railway status
```

### Docker:
```bash
# View logs
docker-compose logs -f app

# Restart services
docker-compose restart

# Stop all
docker-compose down
```

---

## Next Steps

✅ **Test deployment:** Access your app and verify functionality  
✅ **Setup monitoring:** Configure alerts for errors  
✅ **Backup database:** Schedule regular backups

---

**Deployed successfully! 🚀**
