"""Unit tests for scoring service — Bayesian average logic."""

from app.services.scoring import compute_community_score


def test_empty_ratings():
    assert compute_community_score([]) == 0.0


def test_single_perfect_rating():
    score = compute_community_score([5.0])
    assert 0 < score < 100  # Bayesian pulls toward prior

def test_many_perfect_ratings():
    score = compute_community_score([5.0] * 100)
    assert score > 90.0  # Should approach 100


def test_all_lowest_ratings():
    score = compute_community_score([1.0] * 100)
    assert score < 10.0


def test_mixed_ratings_midrange():
    score = compute_community_score([3.0] * 50)
    # 3.0 = midpoint of 1-5 → maps to ~50%
    assert 45 < score < 55


def test_score_in_range():
    for ratings in [[1.0], [5.0], [3.0, 4.0, 2.5], []]:
        score = compute_community_score(ratings)
        assert 0.0 <= score <= 100.0
