"""
Helper functions for user ID resolution
"""
from sqlalchemy.orm import Session
from app.models import User
from fastapi import HTTPException


def get_user_by_id(user_id: str, db: Session) -> User:
    """
    Resolve user_id (can be unique_id or integer id) to User object
    
    Args:
        user_id: User unique ID (16-char) or integer ID
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If user not found
    """
    # Try unique_id first (most common case)
    user = db.query(User).filter(User.unique_id == user_id).first()
    
    if not user:
        # Try integer ID for backwards compatibility
        try:
            int_id = int(user_id)
            user = db.query(User).filter(User.id == int_id).first()
        except ValueError:
            pass
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


def get_user_int_id(user_id: str, db: Session) -> int:
    """
    Convert unique_id or int id to integer id (for foreign keys)
    
    Args:
        user_id: User unique ID or integer ID
        db: Database session
        
    Returns:
        Integer user ID for database operations
    """
    user = get_user_by_id(user_id, db)
    return user.id
