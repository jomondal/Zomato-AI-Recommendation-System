def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    body = response.json()
    assert body["phase"] == "5"
    assert body["llm"] == "groq"
    assert "rate_limit" in body


def test_recommend_endpoint(client):
    response = client.post(
        "/api/v1/recommend",
        json={
            "city": "Banashankari",
            "min_rating": 4.0,
            "max_price": 700,
            "cuisines": ["Italian"],
            "limit": 5,
            "use_llm": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "rule_based"
    assert body["total_candidates"] == 1
    assert len(body["recommendations"]) == 1
    assert body["recommendations"][0]["name"] == "Onesta"
    assert body["latency_ms"] < 200


def test_list_restaurants_endpoint(client):
    response = client.get("/api/v1/restaurants", params={"city": "Banashankari"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert len(body["items"]) == 3


def test_get_restaurant_by_id(client, db_session):
    from sqlalchemy import select

    from shared.db.models import Restaurant

    onesta = db_session.scalar(select(Restaurant).where(Restaurant.name == "Onesta"))
    response = client.get(f"/api/v1/restaurants/{onesta.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Onesta"


def test_get_restaurant_not_found(client):
    response = client.get("/api/v1/restaurants/999")
    assert response.status_code == 404


def test_stats_overview(client):
    response = client.get("/api/v1/stats/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["total_restaurants"] == 3
    assert body["total_cities"] == 1


def test_stats_filtered(client):
    response = client.get(
        "/api/v1/stats/filtered",
        params={"city": "Banashankari", "min_rating": 4.0, "max_price": 700, "cuisines": ["Italian"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total_restaurants"] == 1
    assert body["total_cities"] == 1


def test_stats_cities_and_cuisines(client):
    cities = client.get("/api/v1/stats/cities")
    cuisines = client.get("/api/v1/stats/cuisines")
    assert cities.status_code == 200
    assert cuisines.status_code == 200
    assert cities.json()["items"][0]["city"] == "Banashankari"


def test_filter_options_endpoint(client):
    response = client.get("/api/v1/filters/options")
    assert response.status_code == 200
    body = response.json()
    assert "Banashankari" in body["cities"]
    assert "Italian" in body["cuisines"]
    assert len(body["price_ranges"]) >= 1
