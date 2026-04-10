"""Auth router — register, login, token refresh."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, status

from app.config import get_settings
from app.limiter import limiter
from app.models.schemas import LoginRequest, TokenResponse, UserCreate, UserOut
from app.services.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory user store for v1 (swap for DB in v2)
_users: dict[str, dict] = {}
_email_index: dict[str, str] = {}


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(get_settings().rate_limit_auth)
def register(request: Request, body: UserCreate):
    if body.email in _email_index:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    _users[user_id] = {
        "id": user_id,
        "email": body.email,
        "hashed_password": hash_password(body.password),
        "display_name": body.display_name,
        "created_at": now,
    }
    _email_index[body.email] = user_id
    return UserOut(id=user_id, email=body.email, display_name=body.display_name, created_at=now)


@router.post("/token", response_model=TokenResponse)
@limiter.limit(get_settings().rate_limit_auth)
def login(request: Request, body: LoginRequest):
    user_id = _email_index.get(body.email)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = _users[user_id]
    if not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token, expires_in = create_access_token(subject=user_id)
    return TokenResponse(access_token=token, expires_in=expires_in)
