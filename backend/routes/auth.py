from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import jwt
from database.database import get_db
from services.auth_service import authenticate_google_user, get_user_by_id
from services.jwt_service import decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


class GoogleAuthRequest(BaseModel):
    credential: str = Field(..., min_length=1)


@router.post("/google")
def google_login(request: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Verify Google credential and return app JWT + user profile."""
    print("[auth/google] POST /auth/google received")
    return authenticate_google_user(db, request.credential)


@router.get("/me")
def get_current_user_profile(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
):
    """Return the authenticated user's profile."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Session expired") from exc

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
    }
