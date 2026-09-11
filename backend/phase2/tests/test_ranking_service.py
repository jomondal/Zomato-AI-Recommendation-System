from phase2.services.ranking_service import build_highlights, build_reason, compute_rank_score, to_match_score
from shared.db.models import Restaurant


def test_compute_rank_score_prefers_higher_rating_and_votes():
    popular = Restaurant(name="A", rating=4.6, votes=2556)
    niche = Restaurant(name="B", rating=4.6, votes=10)
    assert compute_rank_score(popular) > compute_rank_score(niche)


def test_to_match_score_scales_to_percentage():
    assert to_match_score(5.0, 10.0) == 50
    assert to_match_score(10.0, 10.0) == 100


def test_build_reason_and_highlights():
    restaurant = Restaurant(
        name="Onesta",
        rating=4.6,
        votes=2556,
        cuisines="Pizza, Cafe, Italian",
        cost_for_two=600,
        location="Banashankari",
        online_order=True,
        cuisine_tags='["Pizza", "Cafe", "Italian"]',
    )
    reason = build_reason(restaurant)
    highlights = build_highlights(restaurant)

    assert "4.6" in reason
    assert "2556" in reason
    assert "₹600" in highlights[1]
    assert "Online order" in highlights
