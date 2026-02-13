from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.database import engine, Base
from app.config import settings
from app.api import routes, auth, inventory, prices
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Track your CS2 inventory and P&L with real-time prices",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
app.include_router(prices.router, prefix="/api/prices", tags=["prices"])
app.include_router(routes.router, prefix="/api", tags=["api"])

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve frontend homepage"""
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return """
    <html>
        <head><title>CS2 Tracker</title></head>
        <body>
            <h1>CS2 Trading Tracker API</h1>
            <p>
                <a href="/docs">API Documentation</a> | 
                <a href="/api/health">Health Check</a>
            </p>
        </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "debug": settings.debug
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
