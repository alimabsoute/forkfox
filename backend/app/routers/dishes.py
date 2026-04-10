"""Dishes router — list, detail, and scoring endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.config import get_settings
from app.deps import optional_auth, require_auth
from app.limiter import limiter
from app.models.schemas import DishListResponse, DishOut, DishScoreRequest, DishScoreResponse
from app.services.scoring import build_score_response, compute_community_score

router = APIRouter(prefix="/dishes", tags=["dishes"])

# In-memory dish store for v1
_dishes: dict[str, dict] = {
    "dish-001": {
        "id": "dish-001",
        "name": "Margherita Pizza",
        "restaurant_name": "Napoli Corner",
        "cuisine_type": "Italian",
        "image_url": None,
        "created_at": datetime(2025, 1, 1, tzinfo=timezone.utc),
        "ratings": [4.5, 5.0, 4.0, 3.5, 4.8],
    },
    "dish-002": {
        "id": "dish-002",
        "name": "Pad Thai",
        "restaurant_name": "Thai Garden",
        "cuisine_type": "Thai",
        "image_url": None,
        "created_at": datetime(2025, 1, 15, tzinfo=timezone.utc),
        "ratings": [4.0, 3.5, 4.5],
    },
}


def _to_dish_out(d: dict) -> DishOut:
    ratings = d.get("ratings", [])
    return DishOut(
        id=d["id"],
        name=d["name"],
        restaurant_name=d["restaurant_name"],
        cuisine_type=d["cuisine_type"],
        community_score=compute_community_score(ratings) if ratings else None,
        rating_count=len(ratings),
        image_url=d.get("image_url"),
        created_at=d["created_at"],
    )


@router.get("", response_model=DishListResponse)
@limiter.limit(get_settings().rate_limit_default)
def list_dishes(
    request: Request,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    cuisine: str | None = Query(default=None),
    _user_id: str | None = Depends(optional_auth),
):
    all_dishes = list(_dishes.values())
    if cuisine:
        all_dishes = [d for d in all_dishes if d["cuisine_type"].lower() == cuisine.lower()]
    total = len(all_dishes)
    start = (page - 1) * page_size
    page_items = all_dishes[start : start + page_size]
    return DishListResponse(
        items=[_to_dish_out(d) for d in page_items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{dish_id}", response_model=DishOut)
@limiter.limit(get_settings().rate_limit_default)
def get_dish(request: Request, dish_id: str, _user_id: str | None = Depends(optional_auth)):
    dish = _dishes.get(dish_id)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dish '{dish_id}' not found")
    return _to_dish_out(dish)


@router.post("/{dish_id}/score", response_model=DishScoreResponse)
@limiter.limit(get_settings().rate_limit_scoring)
def score_dish(
    request: Request,
    dish_id: str,
    body: DishScoreRequest,
    user_id: str = Depends(require_auth),
):
    if dish_id != body.dish_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="dish_id mismatch")
    dish = _dishes.get(dish_id)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dish '{dish_id}' not found")
    dish.setdefault("ratings", []).append(body.rating)
    result = build_score_response(dish_id, dish["ratings"], ai_summary=None)
    return DishScoreResponse(**result)
