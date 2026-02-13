from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.steam import SteamService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


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
        logger.info(f"Updated existing user: {user.steam_username} (ID: {user.id})")
    else:
        # Create new user
        user = User(
            steam_id=steam_id,
            steam_username=player_data.get("personaname", f"User_{steam_id[-6:]}"),
            avatar_url=player_data.get("avatarfull", ""),
        )
        db.add(user)
        logger.info(f"Created new user: {user.steam_username}")
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"User logged in successfully: {user.steam_username} (ID: {user.id})")
    
    # Redirect to dashboard with user ID
    base_url = str(request.base_url).rstrip('/')
    return RedirectResponse(url=f"{base_url}/?user_id={user.id}")


@router.get("/logout")
async def logout():
    """Logout user (clear session)"""
    return RedirectResponse(url="/")


@router.get("/user")
async def get_current_user(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Get current user data
    
    Args:
        user_id: User ID from session/query param
        
    Returns:
        User object
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "steam_id": user.steam_id,
        "username": user.steam_username,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
