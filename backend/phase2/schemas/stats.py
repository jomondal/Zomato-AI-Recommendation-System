from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_restaurants: int
    restaurants_with_rating: int
    average_rating: float | None
    average_cost_for_two: float | None
    total_cities: int
    total_cuisines: int


class CityStat(BaseModel):
    city: str
    count: int


class CuisineStat(BaseModel):
    cuisine: str
    count: int


class CityStatsResponse(BaseModel):
    items: list[CityStat]


class CuisineStatsResponse(BaseModel):
    items: list[CuisineStat]


class FilteredStats(BaseModel):
    total_restaurants: int
    average_rating: float | None
    average_cost_for_two: float | None
    total_cities: int
