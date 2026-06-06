import logging
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from models.user import User
from services.jwt_service import create_access_token

logger = logging.getLogger(__name__)

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_ENV_PATH)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "").strip()
GOOGLE_CLOCK_SKEW_SECONDS = 30


def log_google_client_id_on_startup() -> None:
    """Print configured Google client ID when the app starts."""
    if GOOGLE_CLIENT_ID:
        print(f"[auth] GOOGLE_CLIENT_ID loaded: {GOOGLE_CLIENT_ID}")
    else:
        print("[auth] WARNING: GOOGLE_CLIENT_ID is missing or empty")


def _classify_verification_error(exc: Exception) -> str:
    message = str(exc).lower()

    if "audience" in message or "aud" in message:
        return f"Wrong audience: {exc}"
    if "too early" in message:
        return f"Token used too early (clock skew > {GOOGLE_CLOCK_SKEW_SECONDS}s): {exc}"
    if "expired" in message:
        return f"Expired token: {exc}"
    if "signature" in message:
        return f"Invalid signature: {exc}"
    if "issuer" in message or "iss" in message:
        return f"Invalid issuer: {exc}"
    if "segments" in message or "malformed" in message:
        return f"Malformed credential: {exc}"
    if "certificate" in message or "key" in message:
        return f"Certificate/key verification failure: {exc}"

    return f"Google verification failed: {exc}"


def verify_google_token(credential: str) -> dict:
    """Verify Google ID token and return user claims."""
    if not credential or not credential.strip():
        raise HTTPException(status_code=401, detail="Missing credential")

    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not google_client_id:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth is not configured on the server (GOOGLE_CLIENT_ID missing).",
        )

    credential = credential.strip()
    print(f"[auth/google] Credential received: yes")
    print(f"[auth/google] Credential length: {len(credential)}")
    print(f"[auth/google] Credential preview: {credential[:20]}...")
    print(f"[auth/google] google_client_id: {google_client_id}")

    try:
        idinfo = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            google_client_id,
            clock_skew_in_seconds=GOOGLE_CLOCK_SKEW_SECONDS,
        )
    except Exception as exc:
        print("GOOGLE AUTH ERROR:", str(exc))
        traceback.print_exc()
        detail = _classify_verification_error(exc)
        raise HTTPException(status_code=401, detail=detail) from exc

    token_aud = idinfo.get("aud")
    if token_aud != google_client_id:
        detail = (
            f"Wrong audience: token aud={token_aud!r}, "
            f"expected google_client_id={google_client_id!r}"
        )
        print(f"[auth/google] {detail}")
        raise HTTPException(status_code=401, detail=detail)

    issuer = idinfo.get("iss")
    if issuer not in ("accounts.google.com", "https://accounts.google.com"):
        detail = f"Invalid issuer: {issuer!r}"
        print(f"[auth/google] {detail}")
        raise HTTPException(status_code=401, detail=detail)

    email = idinfo.get("email")
    if not email:
        detail = "Google token missing email claim"
        print(f"[auth/google] {detail}")
        raise HTTPException(status_code=401, detail=detail)

    if not idinfo.get("email_verified"):
        detail = f"Email not verified: {email!r}"
        print(f"[auth/google] {detail}")
        raise HTTPException(status_code=401, detail=detail)

    print(f"[auth/google] Token verified for email={email}")
    return idinfo


def authenticate_google_user(db: Session, credential: str) -> dict:
    """Verify Google credential, upsert user, return app JWT and user profile."""
    claims = verify_google_token(credential)

    google_id = claims.get("sub")
    email = claims.get("email")
    name = claims.get("name", email)
    picture = claims.get("picture")

    print(f"Received Google email: {email}")
    print(f"Received Google name: {name}")
    print(f"Received Google picture: {picture}")

    if not google_id:
        raise HTTPException(status_code=401, detail="Google token missing sub (google_id)")

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
    print("Database insert result: success")

    access_token = create_access_token(user.id, user.email)
    print("JWT creation result: success")

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
