from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from phase2.api.deps import get_db
from phase2.schemas.restaurant import RestaurantFilters, RestaurantListResponse, RestaurantOut
from phase2.services.filter_service import count_restaurants, get_restaurant_by_id, paginate_restaurants
from phase2.services.serializers import to_restaurant_out

router = APIRouter(prefix="/api/v1", tags=["restaurants"])


@router.get("/restaurants", response_model=RestaurantListResponse)
def list_restaurants(
    city: str | None = None,
    location: str | None = None,
    min_rating: float | None = Query(None, ge=0, le=5),
    max_rating: float | None = Query(None, ge=0, le=5),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    cuisines: list[str] = Query(default=[]),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> RestaurantListResponse:
    filters = RestaurantFilters(
        city=city,
        location=location,
        min_rating=min_rating,
        max_rating=max_rating,
        min_price=min_price,
        max_price=max_price,
        cuisines=cuisines,
        page=page,
        page_size=page_size,
    )
    total = count_restaurants(db, filters)
    items = paginate_restaurants(db, filters)
    return RestaurantListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[to_restaurant_out(restaurant) for restaurant in items],
    )


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)) -> RestaurantOut:
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return to_restaurant_out(restaurant)
