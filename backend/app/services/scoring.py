"""Dish scoring service — compute community score from ratings."""

import math
from datetime import datetime, timezone


def compute_community_score(ratings: list[float]) -> float:
    """
    Weighted Bayesian average normalized to 0-100.
    Falls back to 0.0 when no ratings exist.
    """
    if not ratings:
        return 0.0
    # Bayesian average with m=10 prior weight and prior mean C=3.0 (neutral)
    m = 10
    C = 3.0
    n = len(ratings)
    avg = sum(ratings) / n
    bayesian = (m * C + n * avg) / (m + n)
    # Normalize from [1,5] to [0,100]
    return round((bayesian - 1) / 4 * 100, 1)


def build_score_response(dish_id: str, ratings: list[float], ai_summary: str | None) -> dict:
    return {
        "dish_id": dish_id,
        "community_score": compute_community_score(ratings),
        "rating_count": len(ratings),
        "ai_summary": ai_summary,
        "scored_at": datetime.now(timezone.utc),
    }
