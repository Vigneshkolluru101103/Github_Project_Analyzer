import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from models.user import User
from services.jwt_service import create_access_token

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def verify_google_token(token: str) -> dict:
    """Verify Google ID token and return user claims."""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth is not configured on the server (GOOGLE_CLIENT_ID missing).",
        )

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid Google token") from exc

    if idinfo.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise HTTPException(status_code=401, detail="Invalid token issuer")

    return idinfo


def authenticate_google_user(db: Session, google_token: str) -> dict:
    """
    Verify Google token, upsert user, return app JWT and user profile.
    """
    claims = verify_google_token(google_token)

    google_id = claims.get("sub")
    email = claims.get("email")
    name = claims.get("name", email)
    picture = claims.get("picture")

    if not google_id or not email:
        raise HTTPException(status_code=401, detail="Google token missing required fields")

    user = db.query(User).filter(User.google_id == google_id).first()

    if user:
        user.email = email
        user.name = name
        user.picture = picture
        user.last_login_at = datetime.now(timezone.utc)
    else:
        user = User(
            google_id=google_id,
            email=email,
            name=name,
            picture=picture,
            last_login_at=datetime.now(timezone.utc),
        )
        db.add(user)

    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id, user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
        },
    }


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
