from pydantic import BaseModel


class PriceRangeOption(BaseModel):
    label: str
    min: int
    max: int


class RatingRange(BaseModel):
    min: float
    max: float


class FilterOptionsResponse(BaseModel):
    cities: list[str]
    locations: list[str]
    cuisines: list[str]
    price_ranges: list[PriceRangeOption]
    rating_range: RatingRange
