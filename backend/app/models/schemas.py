from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


# ---------- Auth ----------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: str = Field(min_length=1, max_length=80)


class UserOut(BaseModel):
    id: str
    email: str
    display_name: str
    created_at: datetime


# ---------- Dishes ----------

class DishScoreRequest(BaseModel):
    dish_id: str
    rating: float = Field(ge=1.0, le=5.0)
    notes: Optional[str] = Field(default=None, max_length=500)
    tags: list[str] = Field(default_factory=list, max_length=10)


class DishScoreResponse(BaseModel):
    dish_id: str
    community_score: float = Field(ge=0.0, le=100.0)
    rating_count: int
    ai_summary: Optional[str] = None
    scored_at: datetime


class DishOut(BaseModel):
    id: str
    name: str
    restaurant_name: str
    cuisine_type: str
    community_score: Optional[float] = None
    rating_count: int = 0
    image_url: Optional[str] = None
    created_at: datetime


class DishListResponse(BaseModel):
    items: list[DishOut]
    total: int
    page: int
    page_size: int
