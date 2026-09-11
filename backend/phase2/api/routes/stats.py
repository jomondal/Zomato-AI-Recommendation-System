from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from phase2.api.deps import get_db
from phase2.schemas.restaurant import RestaurantFilters
from phase2.schemas.stats import CityStatsResponse, CuisineStatsResponse, FilteredStats, OverviewStats
from phase2.services.stats_service import get_filtered_stats, get_overview_stats, get_top_cities, get_top_cuisines

router = APIRouter(prefix="/api/v1/stats", tags=["stats"])


@router.get("/overview", response_model=OverviewStats)
def overview(db: Session = Depends(get_db)) -> OverviewStats:
    return get_overview_stats(db)


@router.get("/filtered", response_model=FilteredStats)
def filtered(
    city: str | None = None,
    location: str | None = None,
    min_rating: float | None = Query(None, ge=0, le=5),
    max_rating: float | None = Query(None, ge=0, le=5),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    cuisines: list[str] = Query(default=[]),
    db: Session = Depends(get_db),
) -> FilteredStats:
    filters = RestaurantFilters(
        city=city,
        location=location,
        min_rating=min_rating,
        max_rating=max_rating,
        min_price=min_price,
        max_price=max_price,
        cuisines=cuisines,
    )
    return get_filtered_stats(db, filters)


@router.get("/cities", response_model=CityStatsResponse)
def cities(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)) -> CityStatsResponse:
    return CityStatsResponse(items=get_top_cities(db, limit=limit))


@router.get("/cuisines", response_model=CuisineStatsResponse)
def cuisines(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)) -> CuisineStatsResponse:
    return CuisineStatsResponse(items=get_top_cuisines(db, limit=limit))
