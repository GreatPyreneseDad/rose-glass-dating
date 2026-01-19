"""
Authentication Service - Clerk JWT Validation
"""

from fastapi import Header, HTTPException
from typing import Optional
import jwt
import logging

logger = logging.getLogger(__name__)


class User:
    """Authenticated user"""
    def __init__(self, id: str, clerk_id: str, email: str):
        self.id = id
        self.clerk_id = clerk_id
        self.email = email


async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> User:
    """
    Extract and validate user from Clerk JWT token.

    For development/testing, accepts:
    - Authorization: Bearer <clerk_jwt>
    - Authorization: dev_test_user (returns test user)
    """

    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Development mode - allow test user
    if authorization == "dev_test_user":
        logger.info("Using development test user")
        return User(
            id="test-user-id",
            clerk_id="dev_test_clerk_id",
            email="test@roseglass.dating"
        )

    # Extract token
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    # Validate JWT (simplified for MVP - add proper Clerk validation in production)
    try:
        # In production, verify against Clerk's JWKS
        # For MVP, we'll decode without verification (ONLY FOR DEVELOPMENT)
        payload = jwt.decode(token, options={"verify_signature": False})

        clerk_id = payload.get("sub")
        email = payload.get("email")

        if not clerk_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        logger.info(f"Authenticated user: {clerk_id}")

        # In production, get user from database
        # For MVP, return user from token
        return User(
            id=clerk_id,  # Use clerk_id as id for now
            clerk_id=clerk_id,
            email=email or "unknown@roseglass.dating"
        )

    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")
