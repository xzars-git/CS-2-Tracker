from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.steam import SteamService
from datetime import datetime
import logging
import secrets
import string

logger = logging.getLogger(__name__)
router = APIRouter()


def generate_unique_id(length=16):
    """Generate a unique 16-character alphanumeric ID"""
    alphabet = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))


@router.get("/login")
async def steam_login(request: Request):
    """
    Initiate Steam OpenID login
    
    Redirects user to Steam login page
    """
    steam_service = SteamService()
    
    # Build return URL
    base_url = str(request.base_url).rstrip('/')
    return_url = f"{base_url}/api/auth/callback"
    
    # Get Steam login URL
    login_url = steam_service.get_login_url(return_url)
    
    return RedirectResponse(url=login_url)


@router.get("/callback")
async def steam_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle Steam OpenID callback
    
    Validates login and creates/updates user in database
    """
    steam_service = SteamService()
    
    # Get query parameters
    query_params = dict(request.query_params)
    
    logger.info(f"Steam callback received with {len(query_params)} params")
    
    # Verify login
    steam_id = steam_service.verify_login(query_params)
    
    if not steam_id:
        logger.error("Steam login verification failed")
        raise HTTPException(status_code=400, detail="Invalid Steam login. Please try again.")
    
    logger.info(f"Steam login verified for Steam ID: {steam_id}")
    
    # Get player summary
    try:
        player_data = await steam_service.get_player_summary(steam_id)
    except Exception as e:
        logger.error(f"Exception fetching player summary: {e}")
        player_data = None
    
    # Fallback: Create user with minimal data if API fails
    if not player_data:
        logger.warning(f"Failed to fetch player data for {steam_id}, using fallback")
        player_data = {
            "personaname": f"User_{steam_id[-6:]}",  # Use last 6 digits of Steam ID
            "avatarfull": ""
        }
    
    # Check if user exists
    user = db.query(User).filter(User.steam_id == steam_id).first()
    
    if user:
        # Update existing user
        user.steam_username = player_data.get("personaname", user.steam_username)
        user.avatar_url = player_data.get("avatarfull", user.avatar_url)
        user.updated_at = datetime.utcnow()
        logger.info(f"Updated existing user: {user.steam_username} (Unique ID: {user.unique_id})")
    else:
        # Create new user with unique ID
        unique_id = generate_unique_id(16)
        user = User(
            unique_id=unique_id,
            steam_id=steam_id,
            steam_username=player_data.get("personaname", f"User_{steam_id[-6:]}"),
            avatar_url=player_data.get("avatarfull", ""),
        )
        db.add(user)
        logger.info(f"Created new user: {user.steam_username} (Unique ID: {unique_id})")
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"User logged in successfully: {user.steam_username} (Unique ID: {user.unique_id})")
    
    # Redirect to dashboard with unique ID (NOT integer id)
    base_url = str(request.base_url).rstrip('/')
    return RedirectResponse(url=f"{base_url}/?user_id={user.unique_id}")


@router.get("/logout")
async def logout():
    """Logout user (clear session)"""
    return RedirectResponse(url="/")


@router.get("/user")
async def get_current_user(user_id: str = Query(...), db: Session = Depends(get_db)):
    """
    Get current user data
    
    Args:
        user_id: User unique ID (16-char alphanumeric)
        
    Returns:
        User object
    """
    # Try to find by unique_id first, fallback to integer id for backwards compatibility
    user = db.query(User).filter(User.unique_id == user_id).first()
    
    if not user:
        # Try integer ID for old users
        try:
            int_id = int(user_id)
            user = db.query(User).filter(User.id == int_id).first()
        except ValueError:
            pass
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "unique_id": user.unique_id,
        "steam_id": user.steam_id,
        "username": user.steam_username,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
